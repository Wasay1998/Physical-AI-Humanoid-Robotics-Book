# API Contracts for "Create AI Textbook"

This document clarifies the API contracts for the AI Textbook feature.

## No REST/GraphQL API

This project is a content generation project for a Docusaurus website. As such, it does not expose any runtime REST or GraphQL APIs.

The "contracts" for this project are:

1.  **Docusaurus CLI**: The Docusaurus command-line interface is used to build and serve the website.
2.  **File and Directory Structure**: The content and configuration must follow the structure expected by Docusaurus. This is defined in the `plan.md` and `data-model.md`.
3.  **Markdown Frontmatter**: Each markdown file must contain the required frontmatter fields for Docusaurus to render it correctly.
