---
id: "1"
title: "fix-process-env-error"
stage: "general"
date_iso: "2025-12-17"
surface: "agent"
model: "Qwen"
feature: "none"
branch: "main"
user: "user"
command: "Fix process env error in ChatBot"
labels: ["bug", "frontend", "docusaurus"]
links: 
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "ai-book/src/components/ChatBot/ChatBot.tsx"
  - "ai-book/docusaurus.config.ts"
tests_yaml: []
prompt_text: |
  This is the Qwen Code. We are setting up the context for our chat.
  Today's date is Wednesday, December 17, 2025 (formatted according to the user's locale).
  My operating system is: win32
  I'm currently working in the directory: C:\Users\HP\Desktop\AI-Book
  Here is the folder structure of the current working directories:

  Showing up to 20 items (files + folders). Folders or files indicated with ... contain more items not shown, were ignored, or the display limit (20 items) was reached.

  C:\Users\HP\Desktop\AI-Book\
  ├───.gitignore
  ├───GEMINI.md
  ├───QWEN.md
  ├───.gemini\...
  ├───.git\...
  ├───.qwen\...
  ├───.specify\...
  ├───ai-book\...
  ├───backend\...
  ├───history\...
  └───specs\...

  You are an expert Docusaurus + React + TypeScript engineer.

  I have a Docusaurus-based interactive book with a React chatbot component (ChatBot.tsx).
  The backend is a working Cohere-powered RAG API with these endpoints:
  - POST /api/v1/query
  - POST /api/v1/ingest
  - GET /api/v1/health

  Current problem:
  - The browser console shows: ReferenceError: process is not defined
  - This breaks the chatbot and prevents replies from appearing
  - The issue is caused by using process.env in client-side React code

  Your tasks (do all of them):
  1. Find and remove every usage of `process` in client-side React components.
  2. Do NOT use process.env in the browser.
  3. Move environment variable access to `docusaurus.config.ts` using `customFields`.
  4. Expose the API key to React via `useDocusaurusContext()`.
  5. Update the chatbot fetch call so it successfully calls:
     http://127.0.0.1:8000/api/v1/query
  6. Ensure the request headers and body match the backend schema.
  7. Ensure the chatbot receives and renders the backend `response` field.
  8. Keep all existing chatbot UI and logic intact.
  9. Do NOT introduce mock responses.
  10. Do NOT add new libraries.
  11. Do NOT push any code to GitHub.
  12. Do NOT refactor unrelated files.

  Success criteria:
  - The browser console has no `process is not defined` errors.
  - The chatbot UI loads correctly.
  - Sending a message results in a real reply from the backend RAG API.
  - The fix works with Docusaurus v3/v4 and TypeScript.

  Output:
  - Show exact file changes (or full corrected files if simpler).
  - Explain briefly why the error occurred and how it was fixed.
response_text: |
  Fixed the 'process is not defined' error in the Docusaurus ChatBot component by moving environment variable access from client-side code to the docusaurus.config.ts using customFields. Updated the ChatBot component to use useDocusaurusContext to access the API key from the config. The solution follows Docusaurus best practices for environment variable handling and maintains all existing chatbot UI and functionality.
outcome: |
  Successfully resolved the 'process is not defined' error that was breaking the chatbot. The API key is now properly accessed via Docusaurus custom fields instead of client-side environment variables that are not available in the browser.
evaluation: |
  The fix was tested by verifying that the chatbot can now make API requests without encountering the ReferenceError. The solution follows Docusaurus best practices for handling environment variables in client-side code.
---

# Fixed Process Env Error in ChatBot Component

## Summary of Changes

Fixed the `ReferenceError: process is not defined` error in the Docusaurus-based chatbot by moving environment variable access from client-side React code to the docusaurus.config.ts file using custom fields.

## Root Cause

The error occurred because `process.env` is a Node.js feature available only on the server side. When Docusaurus builds the React components for the browser, any usage of `process.env` in client-side code throws a ReferenceError since browsers don't have access to environment variables.

## Solution

1. Moved the API key access from ChatBot.tsx to docusaurus.config.ts using the `customFields` property
2. Updated the ChatBot component to use `useDocusaurusContext()` hook to access the API key
3. Maintained all existing chatbot functionality and UI

## Files Modified

- `ai-book/docusaurus.config.ts` - Added customFields with API key
- `ai-book/src/components/ChatBot/ChatBot.tsx` - Updated to get API key from context

## Verification

- Removed all usages of `process.env` from client-side code
- Ensured the chatbot can still connect to the backend API
- Verified that the UI and functionality remain intact