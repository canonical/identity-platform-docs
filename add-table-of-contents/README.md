# add-table-of-contents

This python script adds a table of contents section to markdown files. The TOC is constructed from the headers, and it is nested according to the header levels.

## Configuration

The script can be configured using the following environment variables:

| Variable name | Description |
|---------------|-----------------------------------------------------------------------------------------|
| `TOC_INPUT`   | Path to a directory containing Markdown files to add table of contents to.               |
| `TOC_OUTPUT`  | Path to a directory where the edited Markdown files will be available.                  |

## Usage

```bash
export TOC_INPUT=./input_docs
export TOC_OUTPUT=./output_docs


python3 ./add-table-of-contents/main.py
```