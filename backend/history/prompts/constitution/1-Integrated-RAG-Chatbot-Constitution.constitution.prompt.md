---
id: 1
title: Integrated-RAG-Chatbot-Constitution
stage: constitution
date: 2025-12-16
surface: agent
model: gpt-4
feature: none
branch: main
user: user
command: /sp.constitution
labels: [constitution,rag,chatbot,book-integration]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution Project: Integrated RAG Chatbot Development for Interactive Book
Core principles:

Functionality-first design with seamless integration into digital book formats
High accuracy in responses by prioritizing relevant retrieval and context-aware generation
User-centric experience (intuitive querying, support for selected text, low-latency responses)
Modularity and maintainability using best practices in code structure
Cost-efficiency leveraging free tiers and open-source tools

Key standards:

All responses must be based on book content or user-selected text; no hallucination without clear sourcing
Use Cohere API exclusively for embeddings and generation (via cohere-python SDK); avoid any OpenAI dependencies
Code quality: PEP 8 compliant, with unit tests for retrieval, generation, and API endpoints
Security: API key handling via environment variables, input validation to prevent injections
Performance: Response time under 2 seconds for queries; relevance scoring >0.7 threshold in Qdrant searches
Documentation: Inline comments, README with setup instructions, and deployment guide

Constraints:

Tech stack: Cohere API, FastAPI, Neon Serverless Postgres, Qdrant Cloud Free Tier, SpecifyPlus Kit for scaffolding, Qwen CLI for prototyping
Book integration: Support for web-based (iframe/JS) or ePub/PDF embedding
Data handling: Book content chunked at 512 tokens max; embeddings via Cohere's embed-v3 model
Development timeline: Modular phases (ingestion, backend, frontend integration, testing)
Budget: Free tiers only; no paid upgrades unless specified

Success criteria:

Chatbot accurately answers 95% of test queries on sample book content
Handles selected text queries without leaking external context
Fully deployable demo with embedded chatbot in a sample book
Zero critical bugs in production simulation
Positive user feedback on response quality and usability in beta testing
```

## Response snapshot

The project constitution has been successfully created with the following details:

**New Version**: 1.0.0 (Initial version)
**Bump Rationale**: This is the initial constitution for the Integrated RAG Chatbot Development for Interactive Book project, establishing core principles and guidelines.

**Files Updated**:
- `.specify/memory/constitution.md` - Contains the complete constitution with all project-specific principles and constraints

**Follow-up Items**: None required at this time

**Suggested Commit Message**: `docs: initial constitution for Integrated RAG Chatbot Development project`

The constitution reflects all the core principles and standards you provided, including functionality-first design, high-accuracy responses, user-centric experience, modularity and maintainability, cost-efficiency, and security. It also incorporates the specified tech stack, performance requirements, and success criteria.

## Outcome

- ✅ Impact: Created initial project constitution from user specifications
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: NA
- 🧠 Reflection: Successfully transformed project specifications into a structured constitution document

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): NA
- Prompt variant (if applicable): NA
- Next experiment (smallest change to try): NA