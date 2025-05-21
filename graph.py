"""
LangGraph definition for the browser automation agent.
"""
from typing import Dict, Any, TypedDict, Annotated
import asyncio
from langgraph.graph import StateGraph
from browser_utils import open_browser_and_navigate

# Define the state schema
class BrowserState(TypedDict):
    url: str
    status: str
    message: str

# Define the node function
async def open_browser_node(state: BrowserState) -> BrowserState:
    """
    Node that opens a browser and navigates to the URL in the state.
    """
    url = state["url"]
    result = await open_browser_and_navigate(url)
    
    return {
        "url": url,
        "status": result["status"],
        "message": result["message"]
    }

# Create the graph
def create_browser_graph() -> StateGraph:
    """
    Creates a LangGraph for browser automation.
    """
    # Initialize the graph
    graph = StateGraph(BrowserState)
    
    # Add the node
    graph.add_node("open_browser", open_browser_node)
    
    # Set the entry point
    graph.set_entry_point("open_browser")
    
    # Compile the graph
    return graph.compile()

# Function to invoke the graph with a URL
async def run_browser_graph(url: str) -> Dict[str, Any]:
    """
    Runs the browser graph with the provided URL.
    
    Args:
        url: The URL to navigate to
        
    Returns:
        The final state of the graph
    """
    # Create the graph
    graph = create_browser_graph()
    
    # Initialize the state
    initial_state = {
        "url": url,
        "status": "pending",
        "message": "Starting browser automation"
    }
    
    # Run the graph
    result = await graph.ainvoke(initial_state)
    
    return result
