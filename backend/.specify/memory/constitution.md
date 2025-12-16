<!-- 
SYNC IMPACT REPORT
Version change: N/A (new constitution) → 1.0.0
Added sections: All sections as this is a new constitution for this project
Removed sections: N/A
Modified principles: N/A (first version)
Templates requiring updates: 
- ✅ plan-template.md: No specific constitution references to update
- ✅ spec-template.md: No specific constitution references to update  
- ✅ tasks-template.md: No specific constitution references to update
- ⚠ No command files found that need updating
- ⚠ README.md does not exist to update
No placeholders intentionally deferred.
-->

# Integrated RAG Chatbot Development for Interactive Book Constitution

## Core Principles

### Functionality-First Design
Every feature starts with a clear focus on functionality that integrates seamlessly into digital book formats; user experience guides all implementation decisions; solutions must enhance the core reading experience.

### High-Accuracy Responses
Prioritize relevant retrieval and context-aware generation to ensure high accuracy; all responses must be based on book content or user-selected text; no hallucination without clear sourcing.

### User-Centric Experience
Design for intuitive querying, support for selected text, and low-latency responses; focus on accessibility and ease of use for all users interacting with the digital book interface.

### Modularity and Maintainability
Use best practices in code structure, with clear separation of concerns; ensure components are independently testable and reusable across different book integration scenarios.

### Cost-Efficiency
Leverage free tiers and open-source tools to maximize value; prioritize solutions that remain accessible to users with limited resources while maintaining quality.

### Security and Compliance
Implement secure API key handling via environment variables; ensure input validation to prevent injections; maintain privacy and data protection standards.

## Key Standards and Constraints
Use Cohere API exclusively for embeddings and generation (via cohere-python SDK); avoid any OpenAI dependencies. Code quality: PEP 8 compliant, with unit tests for retrieval, generation, and API endpoints. Tech stack: Cohere API, FastAPI, Neon Serverless Postgres, Qdrant Cloud Free Tier, SpecifyPlus Kit for scaffolding, Qwen CLI for prototyping. Book integration: Support for web-based (iframe/JS) or ePub/PDF embedding. Data handling: Book content chunked at 512 tokens max; embeddings via Cohere's embed-v3 model.

## Performance and Success Criteria
Performance: Response time under 2 seconds for queries; relevance scoring >0.7 threshold in Qdrant searches. Success criteria: Chatbot accurately answers 95% of test queries on sample book content; handles selected text queries without leaking external context; fully deployable demo with embedded chatbot in a sample book; zero critical bugs in production simulation; positive user feedback on response quality and usability in beta testing.

## Governance
All implementations must verify compliance with the core principles; All PRs must include tests covering new functionality; Code reviews must verify adherence to tech stack constraints; Amendments require documentation and approval.

**Version**: 1.0.0 | **Ratified**: 2025-12-16 | **Last Amended**: 2025-12-16