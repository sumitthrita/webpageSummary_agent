# Website Summarization Agent with LangGraph

This project implements an agent using the LangGraph framework that opens a browser, navigates to a specified URL, extracts the content, and generates a summary using Claude (Anthropic's LLM). The agent is exposed via a FastAPI endpoint.

## Project Structure

- `app.py`: FastAPI application with the API endpoints
- `graph.py`: LangGraph definition with the website summarization workflow
- `browser_utils.py`: Utility functions for browser automation, text extraction, and summary generation
- `.env`: Environment variables file containing the Anthropic API key

## Requirements

- Python 3.8+
- Virtual environment (venv)
- Dependencies: langgraph, fastapi, uvicorn, playwright, langchain-community, anthropic
- Anthropic API key (stored in .env file)

## Setup

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the required packages:
   ```
   pip install langgraph fastapi uvicorn playwright langchain-community anthropic
   ```

3. Install Playwright browsers:
   ```
   playwright install chromium
   ```

4. Create a `.env` file with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Running the Application

Start the FastAPI server:
```
python app.py
```

The server will start on http://0.0.0.0:8000.

## LangGraph Workflow

The application uses LangGraph to define a workflow with the following nodes:

1. `open_browser_node`: Opens a browser and navigates to the specified URL
2. `extract_text_node`: Extracts text content from the website using PlayWrightBrowserToolkit
3. `generate_summary_node`: Generates a summary of the website content using Claude

## API Endpoints

### POST /summarize-website

Opens a browser, navigates to the specified URL, extracts the content, and generates a summary.

Request body:
```json
{
  "url": "https://example.com"
}
```

Response:
```json
{
  "url": "https://example.com",
  "status": "success",
  "message": "Successfully generated summary",
  "summary": "This is a summary of the website content..."
}
```

### GET /health

Health check endpoint.

Response:
```json
{
  "status": "healthy"
}
```

## Testing the API

You can test the API using curl:

```bash
curl -X POST http://localhost:8000/summarize-website \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

Or using the FastAPI Swagger UI at http://localhost:8000/docs.

## How It Works

1. The user provides a URL to the API
2. The LangGraph workflow is triggered:
   - A browser is opened and navigates to the URL
   - The PlayWrightBrowserToolkit extracts text content from the website
   - Claude (Anthropic's LLM) generates a summary of the content
3. The summary is returned to the user

The workflow is defined as a directed graph with nodes for each step and edges that determine the flow between steps.
