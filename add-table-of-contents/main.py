import os
import re

"""Constants"""
INPUT_DIR = os.environ.get('TOC_INPUT')
OUTPUT_DIR = os.environ.get('TOC_OUTPUT')

HEADER_MATCH = "^#+"
NAVIGATION_MATCH = "Navigation"

PHASE_PRE_HEADER = 0
PHASE_POST_HEADER = 1

ANCHOR_TEMPLATE = '<a href="#{0}"><h{1} id="{0}">{2}</h{1}></a>\n'
TOC_TEMPLATE = '* [{}](#{})\n'


def main():
    for entry in os.scandir(INPUT_DIR):
        if entry.is_file() and entry.name.endswith(".md"):
            processDoc(entry)


def getAnchorID(id: int):
    desired_width = 4
    return "{:0>{}}".format(id, desired_width)


def isUsefulHeader(line: str):
    """The TOC is made up of the headers, with the exception of the Navigation header"""

    header = re.findall(HEADER_MATCH, line)
    not_navigation = not re.findall(NAVIGATION_MATCH, line)
    if header and not_navigation:
        return (True, len(header[0]))
    return (False, 0)


def constructTOC(anchorList):
    """Renders markdown of TOC with nested lists"""

    if not anchorList:
        return []

    tocList = ["**Contents:**\n"]
    startHeaderLevel = 1
    start = True

    for (item, anchor, header) in anchorList:
        if start:
            start = False
            startHeaderLevel = header
            tocList.append(TOC_TEMPLATE.format(item, anchor))
        else:
            checkHeader = header
            indentLevel = checkHeader - startHeaderLevel
            if indentLevel < 0:
                indentLevel = 0
            toc = "  " * indentLevel + TOC_TEMPLATE.format(item, anchor)

            tocList.append(toc)

    tocList.append("\n")
    return tocList


def processDoc(doc):
    """Collects headers, and creates new markdown with the TOC after the first paragraph."""
    phase = PHASE_PRE_HEADER
    firstParagraph = []
    content = []
    anchorList = []
    anchorCounter = 0

    with open(doc.path, "r") as lines:
        for line in lines:
            ok, mkHeader = isUsefulHeader(line)
            if phase == PHASE_PRE_HEADER:
                if ok:
                    anchorString = getAnchorID(anchorCounter)
                    itemString = line.strip("#").strip()
                    anchorCounter += 1

                    content.append(ANCHOR_TEMPLATE.format(anchorString, mkHeader, itemString))
                    anchorList.append((itemString, anchorString, mkHeader))
                    phase = PHASE_POST_HEADER
                else:
                    firstParagraph.append(line)
            else:
                if ok:
                    anchorString = getAnchorID(anchorCounter)
                    itemString = line.strip("#").strip()
                    anchorCounter += 1

                    content.append(ANCHOR_TEMPLATE.format(anchorString, mkHeader, itemString))
                    anchorList.append((itemString, anchorString, mkHeader))
                else:
                    content.append(line)

    toc = constructTOC(anchorList)

    with open(f"{OUTPUT_DIR}/{doc.name}", "w") as output:
        output.writelines(firstParagraph)
        if toc:
            output.writelines(toc)
        if content:
            output.writelines(content)

    return


if __name__ == "__main__":
    main()
