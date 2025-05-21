"""
FastAPI application for the browser automation agent.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from graph import run_browser_graph
import uvicorn

# Create the FastAPI app
app = FastAPI(
    title="Browser Automation Agent",
    description="An agent that opens a browser and navigates to a specified URL",
    version="0.1.0"
)

# Define the request model
class UrlRequest(BaseModel):
    url: HttpUrl

# Define the response model
class BrowserResponse(BaseModel):
    url: str
    status: str
    message: str

# Define the POST endpoint
@app.post("/open-browser", response_model=BrowserResponse)
async def open_browser(request: UrlRequest) -> BrowserResponse:
    """
    Opens a browser and navigates to the specified URL.
    
    Args:
        request: The request containing the URL to navigate to
        
    Returns:
        The result of the browser automation
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
            message=result["message"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running browser automation: {str(e)}"
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
