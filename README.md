# Website Summarization Agent with LangGraph

This project implements an agent using the LangGraph framework that opens a browser, navigates to a specified URL, extracts the content, and generates a summary using Claude (Anthropic's LLM). The agent is available through both a FastAPI endpoint and a Gradio UI.

## Project Structure

- `app.py`: FastAPI application with the API endpoints
- `gradio_app.py`: Gradio UI for the website summarization
- `graph.py`: LangGraph definition with the website summarization workflow
- `browser_utils.py`: Utility functions for browser automation, text extraction, and summary generation
- `.env`: Environment variables file containing the Anthropic API key

## Requirements

- Python 3.8+
- Virtual environment (venv)
- Dependencies: langgraph, fastapi, uvicorn, playwright, langchain-community, anthropic, gradio
- Anthropic API key (stored in .env file)

## Setup

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the required packages:
   ```
   pip install langgraph fastapi uvicorn playwright langchain-community anthropic gradio
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

### Gradio UI (Recommended)

Start the Gradio UI:
```
python gradio_app.py
```

The Gradio UI will start and open in your default web browser. You can enter a URL and click the "Summarize" button to get a summary of the website content.

### FastAPI Server

Alternatively, you can start the FastAPI server:
```
python app.py
```

The server will start on http://0.0.0.0:8000.

## LangGraph Workflow

The application uses LangGraph to define a workflow with the following nodes:

1. `open_browser_node`: Opens a browser and navigates to the specified URL
2. `extract_text_node`: Extracts text content from the website
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

1. The user provides a URL through the Gradio UI or API
2. The LangGraph workflow is triggered:
   - A browser is opened and navigates to the URL
   - Text content is extracted from the website
   - Claude (Anthropic's LLM) generates a summary of the content
3. The summary is displayed in the UI or returned via the API

The workflow is defined as a directed graph with nodes for each step and edges that determine the flow between steps.
