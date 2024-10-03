# Canonical Identity Platform Documentation

[![Discourse Sync](https://github.com/canonical/canonical-identity-platform-docs/actions/workflows/discourse-sync.yaml/badge.svg)](https://github.com/canonical/canonical-identity-platform-docs/actions/workflows/discourse-sync.yaml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196.svg)](https://conventionalcommits.org)

## Description

This repository contains all the documentation related to
the [Canonical Identity Platform](https://charmhub.io/identity-platform).

The documentation is synchronized automatically with the Discord pages for the
Identity Platform bundle.

## Add new documents

First, create pages on Discourse to get their IDs.

For each of the pages:

- Go to [Discourse](https://discourse.charmhub.io/).
- Press New Topic button in the top right corner.
  - Title: `<page-name-with-hyphens>` (should match file name in DOCS).
  - Category: change from `other` to `charm`.
  - Tags: `<charm-name>`, `docs`.
  - Description: anything, it will be replaced by Github automation.
- Press Click Topic.
- Get the numerical page ID from latest segment of the URL.

Add `<page-name>: <page-id>` pairs to topic-ids.yaml.

Create markdown files under DOCS. File names must match page names added to Discourse (`<page-name>.md`).

Don't forget to update the relevant index `DOCS/<charm>.md`.

Open a PR, ask for review, merge. Github automation should take care of the rest.
