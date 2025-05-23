"""
LangGraph definition for the website summarization agent.
"""
from typing import Dict, Any, TypedDict, Annotated, Literal, cast
import asyncio
from langgraph.graph import StateGraph, END
from browser_utils import open_browser_and_navigate, extract_website_text, generate_summary
from langsmith_utils import get_langsmith_client, test_langsmith_connection

# Initialize LangSmith client
langsmith_client = get_langsmith_client()

# Define the state schema
class BrowserState(TypedDict):
    url: str
    status: str
    message: str
    text_content: str
    summary: str

# Define the node functions
async def open_browser_node(state: BrowserState) -> BrowserState:
    """
    Node that opens a browser and navigates to the URL in the state.
    """
    url = state["url"]
    result = await open_browser_and_navigate(url)
    
    return {
        **state,
        "status": result["status"],
        "message": result["message"]
    }

async def extract_text_node(state: BrowserState) -> BrowserState:
    """
    Node that extracts text from the website.
    """
    print(f"[extract_text_node] Starting with URL: {state['url']}")
    url = state["url"]
    result = await extract_website_text(url)
    
    print(f"[extract_text_node] Extraction result status: {result['status']}")
    print(f"[extract_text_node] Extracted text length: {len(result.get('text_content', ''))}")
    
    return {
        **state,
        "status": result["status"],
        "message": result["message"],
        "text_content": result.get("text_content", "")
    }

async def generate_summary_node(state: BrowserState) -> BrowserState:
    """
    Node that generates a summary of the website content.
    """
    print(f"[generate_summary_node] Starting with text content length: {len(state['text_content'])}")
    text_content = state["text_content"]
    result = await generate_summary(text_content)
    
    print(f"[generate_summary_node] Summary generation result status: {result['status']}")
    print(f"[generate_summary_node] Summary length: {len(result.get('summary', ''))}")
    
    return {
        **state,
        "status": result["status"],
        "message": result["message"],
        "summary": result.get("summary", "")
    }

# Create the graph
def create_browser_graph() -> StateGraph:
    """
    Creates a LangGraph for website summarization.
    """
    # Initialize the graph
    graph = StateGraph(BrowserState)
    
    # Add the nodes
    graph.add_node("open_browser", open_browser_node)
    graph.add_node("extract_text", extract_text_node)
    graph.add_node("generate_summary", generate_summary_node)
    
    # Set the entry point
    graph.set_entry_point("open_browser")
    
    # Add the edges - create a simple linear flow
    graph.add_edge("open_browser", "extract_text")
    graph.add_edge("extract_text", "generate_summary")
    graph.add_edge("generate_summary", END)
    
    # Compile the graph
    return graph.compile()

# Function to invoke the graph with a URL
async def run_browser_graph(url: str) -> Dict[str, Any]:
    """
    Runs the website summarization graph with the provided URL.
    
    Args:
        url: The URL to navigate to
        
    Returns:
        The final state of the graph
    """
    # Test LangSmith connection
    print("🔍 Testing LangSmith connection...")
    test_langsmith_connection()
    
    # Create the graph
    graph = create_browser_graph()
    
    # Initialize the state
    initial_state = {
        "url": url,
        "status": "pending",
        "message": "Starting website summarization",
        "text_content": "",
        "summary": ""
    }
    
    # Run the graph
    result = await graph.ainvoke(initial_state)
    
    return result
