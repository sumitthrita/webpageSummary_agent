"""
FastAPI application for the website summarization agent.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from graph import run_browser_graph
import uvicorn

# Create the FastAPI app
app = FastAPI(
    title="Website Summarization Agent",
    description="An agent that opens a browser, navigates to a specified URL, and generates a summary of the website content",
    version="0.2.0"
)

# Define the request model
class UrlRequest(BaseModel):
    url: HttpUrl

# Define the response model
class BrowserResponse(BaseModel):
    url: str
    status: str
    message: str
    summary: str = ""

# Define the POST endpoint
@app.post("/summarize-website", response_model=BrowserResponse)
async def summarize_website(request: UrlRequest) -> BrowserResponse:
    """
    Opens a browser, navigates to the specified URL, and generates a summary of the website content.
    
    Args:
        request: The request containing the URL to navigate to
        
    Returns:
        The result of the website summarization
    """
    try:
        # Convert the URL to a string
        url_str = str(request.url)
        
        # Run the graph
        result = await run_browser_graph(url_str)
        
        # Return the response
        return BrowserResponse(
            url=result["url"],
            status=result["status"],
            message=result["message"],
            summary=result.get("summary", "")
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running website summarization: {str(e)}"
        )

# Add a simple health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}

# Run the app if this file is executed directly
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
