---
id: 1
title: rag-chatbot-book-implementation-plan
stage: plan
date: 2025-12-16
surface: agent
model: "gpt-4"
feature: "001-rag-chatbot-book"
branch: "001-rag-chatbot-book"
user: "HP"
command: "/sp.plan"
labels: ["planning", "architecture", "rag", "cohere", "qdrant"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-rag-chatbot-book/plan.md"
  - "specs/001-rag-chatbot-book/research.md"
  - "specs/001-rag-chatbot-book/data-model.md"
  - "specs/001-rag-chatbot-book/quickstart.md"
  - "specs/001-rag-chatbot-book/contracts/openapi.yaml"
tests:
  - "N/A - Planning phase"
---

# Prompt History Record: RAG Chatbot Book Implementation Plan

## PROMPT_TEXT

```
/sp.plan Project Phase Plan: Integrated RAG Chatbot Development for Interactive Book
(Strictly following the provided /sp.constitution and /sp.specify – Cohere exclusive, free tiers only, secure credentials, high accuracy, embeddable widget)
Phase 1: Secure Project Initialization & Setup  (1-2 days)

Initialize project repository using SpecifyPlus Kit for clean modular structure
Set up Python virtual environment
Install required dependencies: fastapi, uvicorn, cohere, qdrant-client, psycopg2-binary, python-dotenv, pydantic
Create .env file (add to .gitignore) and load the following credentials securely:
COHERE_API_KEY=R2mDS9KZEUHABQ9j6hPn2vogSxq5nBPx2zi0pUvX
QDRANT_URL=https://a61eb060-a82f-4ee2-b942-2a0342e4ff9f.europe-west3-0.gcp.cloud.qdrant.io
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.kEj_NPTK0BwNQytj6yjizattRCGD2D-XwrRgxxZ7nbE
DATABASE_URL=postgresql://neondb_owner:npg_0RLqH8tphdvP@ep-silent-shape-adtn3hxp-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
Write and execute connection test scripts for Cohere API, Qdrant Cloud, and Neon Postgres
Use Qwen CLI for local prototyping and validation of Cohere embedding/generation calls

Phase 2: Book Content Ingestion Pipeline  (2-3 days)

Build ingestion module supporting book input as .txt, .md, or extracted PDF text
Chunk text into segments of maximum 512 tokens with 150-token overlap
Generate embeddings using only Cohere's embed-v3 model (english or multilingual as needed)
Create Qdrant collection named "book_content" with Cosine distance and appropriate vector dimensions
Upload all chunks with metadata (chunk_id, section/page number, original_text)
Store chunk metadata in a Neon Postgres table ("chunks") for citation tracking and fast lookup
Ensure ingestion is idempotent, logged, and includes progress indicators

Phase 3: FastAPI Backend with RAG Logic  (4-5 days)

Develop clean, modular FastAPI application (PEP-8 compliant, full inline documentation)
Implement core endpoints:
POST /ingest (development-only: trigger book ingestion)
POST /query (full-book RAG query)
POST /query-selected (query restricted strictly to user-selected text; no retrieval)
GET /health (status check)

RAG pipeline:
Embed user query with Cohere embed-v3
Search Qdrant with top-k=6-8 and relevance score threshold >0.7
Generate response using Cohere Chat API (command-r-plus preferred) with strict system prompt: answer only from provided context, include citations, refuse hallucination

Return citations (section/page) in every applicable response
Optional lightweight conversation history stored in Neon Postgres
Add robust input validation, error handling, and basic rate limiting

Phase 4: Embeddable Chatbot Frontend Widget  (3-4 days)

Build lightweight chat interface using vanilla HTML/CSS/JavaScript (no heavy frameworks for easy embedding)
Implement text selection feature: user highlights book text → button appears → "Ask about this selection" → sends to /query-selected
Display chat history, loading states, formatted responses, and clickable citations
Design as an embeddable widget (iframe-friendly or script-tag injectable)
Ensure responsive, mobile-friendly, and accessible UI
Test embedding in a sample static HTML book page

Phase 5: Testing, Optimization & Validation  (3-4 days)

Create comprehensive test suite with 50+ queries:
General full-book questions
Selected-text-only questions
Edge cases (empty queries, long selections, irrelevant/out-of-scope attempts)

Target success metrics: ≥95% factual accuracy, response time <2 seconds, relevance scores >0.7
Write unit tests covering ingestion, retrieval, generation, and API endpoints
Optimize chunk size, overlap, top-k, and prompts based on test results
Perform security review: confirm no credential exposure client-side, proper input sanitization

Phase 6: Deployment & Final Demo  (1-2 days)

Deploy FastAPI backend to a free hosting platform (Railway, Render, or Fly.io)
Host static frontend and sample interactive book page
Deliver a complete working demo: sample digital book with fully embedded and functional chatbot
Write detailed README covering setup, ingestion process, usage instructions, limitations, and secure credential handling
Prepare demo screenshots/video showcasing both general queries and selected-text queries

Total Estimated Timeline: 14-20 days (modular, iterative development)
Final Deliverables:

Secure, high-accuracy Cohere-powered RAG backend
Fully embeddable chatbot widget integrated into a sample digital book
Clean, PEP-8 compliant, well-documented codebase with tests
Demonstrated ≥95% accuracy on test queries with proper context isolation
Zero critical bugs in the deployed demo

Strictly Out of Scope (per constitution/specify):

Any OpenAI or alternative LLM usage
Custom LLM training or fine-tuning
Paid services or tier upgrades
Full publishing platform or multi-book support
Non-RAG features (e.g., external search, unrelated tools)
```

## RESPONSE_TEXT

Created a comprehensive implementation plan for the RAG Chatbot project, including:
- Completed the plan.md file with technical context and constitution check
- Created research.md with technology decisions and best practices
- Created data-model.md with entities from the feature spec
- Created API contracts (OpenAPI spec) in the contracts directory
- Created a quickstart guide for onboarding
- Updated agent context (though extraction didn't work as expected due to format issues)

## OUTCOME

Successfully completed all required planning artifacts for the RAG chatbot project in accordance with the specified constitution and requirements, preparing for the implementation phase.

## EVALUATION

All required planning artifacts have been created according to the workflow:
- Plan document with technical context and constitution check
- Research findings
- Data models
- API contracts
- Quickstart guide
- Agent context update