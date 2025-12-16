# Quickstart Guide: Integrated RAG Chatbot for Interactive Books

## Overview
This guide will help you quickly set up and start using the RAG chatbot for interactive books. It covers the essential steps to get your local development environment running and start ingesting and querying book content.

## Prerequisites
- Python 3.11 or higher
- pip package manager
- Git (for version control)
- Access to Cohere API (with an API key)
- Access to Qdrant Cloud (with URL and API key)
- Access to Neon Serverless Postgres (with connection string)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd rag-chatbot-book/backend
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root based on the `.env.example`:
```bash
cp .env.example .env
```

Then populate the `.env` file with your actual credentials:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
DATABASE_URL=your_postgres_connection_string_here
```

## Running the Application

### 1. Start the Development Server
```bash
uvicorn src.api.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

### 2. Access the API Documentation
Once the server is running, you can access the interactive API documentation at:
- `http://localhost:8000/docs` (Swagger UI)
- `http://localhost:8000/redoc` (ReDoc)

## Basic Usage

### 1. Ingest a Book
Use the `/ingest` endpoint to upload and process a book:

```bash
curl -X POST "http://localhost:8000/ingest" \
  -H "X-API-Key: $API_KEY" \
  -F "file=@path/to/your/book.pdf" \
  -F "title=Your Book Title" \
  -F "author=Author Name"
```

You'll receive a response indicating that ingestion has started with the book ID:
```json
{
  "message": "Book ingestion started successfully",
  "book_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "INGESTING"
}
```

### 2. Query the Book
After the book has been indexed, you can query it using the `/query` endpoint:

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "book_id": "550e8400-e29b-41d4-a716-446655440000",
    "query": "What are the main concepts discussed in this book?"
  }'
```

You'll receive a response with the AI-generated answer and citations:
```json
{
  "response": "The main concepts discussed in this book include...",
  "citations": [
    {
      "chunk_id": "chunk_001",
      "page_number": 25,
      "section_title": "Introduction",
      "text_preview": "This book covers the fundamental concepts of..."
    }
  ],
  "session_token": "sess_abc123def456",
  "query_id": "550e8400-e29b-41d4-a716-446655440001",
  "relevance_score": 0.85
}
```

### 3. Query with Selected Text
For queries based on user-selected text, use the `/query-selected` endpoint:

```bash
curl -X POST "http://localhost:8000/query-selected" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "book_id": "550e8400-e29b-41d4-a716-446655440000",
    "query": "Can you explain this concept in simpler terms?",
    "selected_text": "The primary principle of machine learning is learning from data without being explicitly programmed."
  }'
```

## Testing the Application

Run the test suite using pytest:

```bash
pytest
```

To run specific test categories:
- Unit tests: `pytest tests/unit/`
- Integration tests: `pytest tests/integration/`
- Contract tests: `pytest tests/contract/`

## Embedding the Widget

To use the chatbot widget in a web-based book:

1. Include the widget JavaScript in your HTML:
```html
<script src="/path/to/chatbot-widget.js"></script>
```

2. Add the widget container to your page:
```html
<div id="rag-chatbot-widget"></div>
```

3. Initialize the widget:
```javascript
const chatbot = new RagChatbotWidget({
  containerId: 'rag-chatbot-widget',
  apiUrl: 'http://localhost:8000',
  bookId: '550e8400-e29b-41d4-a716-446655440000',
  apiKey: 'your-api-key'
});

chatbot.init();
```

## Development Workflow

### Code Structure
```
backend/
├── src/
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   ├── api/            # API endpoints
│   └── config/         # Configuration
├── tests/              # Test files
├── requirements.txt    # Python dependencies
└── main.py            # Application entry point
```

### Running in Development Mode
Use the `--reload` flag with Uvicorn to automatically restart the server when code changes:
```bash
uvicorn src.api.main:app --reload --port 8000
```

### Adding New Dependencies
1. Add the dependency to `requirements.in`
2. Regenerate `requirements.txt`:
```bash
pip-compile requirements.in
```

## Troubleshooting

### Common Issues

1. **API Key Issues**
   - Ensure your API keys are correctly set in the `.env` file
   - Verify that your keys have the necessary permissions

2. **Qdrant Connection Issues**
   - Check that your Qdrant URL and API key are correct
   - Ensure your network allows connections to the Qdrant instance

3. **Database Connection Issues**
   - Verify your PostgreSQL connection string
   - Check that your Neon Serverless Postgres instance is active

4. **Large File Upload Issues**
   - Check the file size limit in your configuration
   - Ensure your web server can handle large uploads

## Next Steps

1. Explore the API documentation at `/docs` for detailed endpoint information
2. Review the data models in `models/` to understand the system's structure
3. Check the test suite to understand expected behavior
4. Review the architecture documentation for system design details