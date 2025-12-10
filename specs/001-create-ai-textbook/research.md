# Research for "Create AI Textbook"

This document outlines the research performed to resolve unknowns identified in the `plan.md`.

## 1. Testing Strategy



### Decision

A combination of testing strategies will be used:

- **Unit & Component Testing**: Use Jest and React Testing Library for testing individual React components.

- **End-to-End Testing**: Use Cypress or Playwright to test the full user experience, including navigation, page rendering, and interactivity.

- **Linting**: Use ESLint to enforce code quality and style.

- **Markdown Link Checking**: Use a tool to check for broken links in the markdown files.



### Rationale

This multi-layered approach ensures both the underlying code and the user-facing content are correct and functional.

- **Jest/RTL** are industry standards for React testing.

- **Cypress/Playwright** are powerful tools for E2E testing of modern web applications.

- **Linting** and **link checking** are essential for maintaining a high-quality Docusaurus site.



### Alternatives Considered

- **Manual Testing**: Prone to error and not scalable.

- **Only E2E Testing**: Can be slow and doesn't cover all component states.

- **Only Unit Testing**: Doesn't guarantee the application works as a whole.
