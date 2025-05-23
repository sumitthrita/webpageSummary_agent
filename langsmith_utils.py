"""
LangSmith utilities for logging and tracing.
"""
import os
from langsmith import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize LangSmith client
def get_langsmith_client() -> Client:
    """
    Initialize and return a LangSmith client.
    
    Returns:
        LangSmith Client instance
    """
    client = Client()
    return client

# Test function to verify LangSmith connection
def test_langsmith_connection():
    """
    Test the LangSmith client connection by listing runs from the project.
    """
    try:
        client = get_langsmith_client()
        # List runs from the specific project
        project_name = os.getenv("LANGSMITH_PROJECT", "content-summary-agent")
        runs = list(client.list_runs(project_name=project_name, limit=5))
        print(f"✅ LangSmith connection successful! Found {len(runs)} recent runs in project '{project_name}'.")
        return True
    except Exception as e:
        print(f"❌ LangSmith connection failed: {str(e)}")
        return False

# # Function to log custom events - Commented out as LangChain handles logging automatically
# def log_event(client: Client, event_name: str, data: dict):
#     """
#     Log a custom event to LangSmith.
#     
#     Args:
#         client: LangSmith client instance
#         event_name: Name of the event
#         data: Event data to log
#     """
#     try:
#         # You can customize this based on your logging needs
#         print(f"📝 Logging event '{event_name}' with data: {data}")
#         # Additional LangSmith logging logic can be added here
#     except Exception as e:
#         print(f"❌ Failed to log event '{event_name}': {str(e)}")
