# Browser Automation Agent with LangGraph

This project implements a simple agent using the LangGraph framework that opens a Chromium browser and navigates to a specified URL. The agent is exposed via a FastAPI endpoint.

## Project Structure

- `app.py`: FastAPI application with the POST endpoint
- `graph.py`: LangGraph definition with the browser automation node
- `browser_utils.py`: Utility functions for browser automation using Playwright

## Requirements

- Python 3.8+
- Virtual environment (venv)
- Dependencies: langgraph, fastapi, uvicorn, playwright

## Setup

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the required packages:
   ```
   pip install langgraph fastapi uvicorn playwright
   ```

3. Install Playwright browsers:
   ```
   playwright install chromium
   ```

## Running the Application

Start the FastAPI server:
```
python app.py
```

The server will start on http://0.0.0.0:8000.

## API Endpoints

### POST /open-browser

Opens a browser and navigates to the specified URL.

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
  "message": "Successfully opened browser and navigated to https://example.com"
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
curl -X POST http://localhost:8000/open-browser \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

Or using the FastAPI Swagger UI at http://localhost:8000/docs.
