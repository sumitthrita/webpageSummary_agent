"""
Test script to verify LangSmith client integration.
"""
from langsmith import Client
from langsmith_utils import get_langsmith_client, test_langsmith_connection

def main():
    """
    Test the LangSmith client as requested by the user.
    """
    print("🚀 Testing LangSmith Client Integration")
    print("=" * 50)
    
    # Test 1: Basic client initialization
    print("\n1. Testing client initialization...")
    try:
        client = Client()
        print("✅ LangSmith Client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize client: {str(e)}")
        return
    
    # Test 2: List runs (as requested by user)
    print("\n2. Testing client.list_runs()...")
    try:
        import os
        project_name = os.getenv("LANGSMITH_PROJECT", "content-summary-agent")
        runs = list(client.list_runs(project_name=project_name, limit=5))
        print(f"✅ Successfully retrieved {len(runs)} runs from project '{project_name}'")
        if runs:
            print(f"📊 Recent runs: {[run.id for run in runs[:3]]}")  # Show first 3 run IDs
        else:
            print("📊 No runs found in the project yet")
    except Exception as e:
        print(f"❌ Failed to list runs: {str(e)}")
    
    # Test 3: Using our utility functions
    print("\n3. Testing utility functions...")
    client_from_utils = get_langsmith_client()
    print("✅ Client from utils initialized")
    
    # Test 4: Connection test
    print("\n4. Testing connection...")
    test_langsmith_connection()
    
    print("\n" + "=" * 50)
    print("🎉 LangSmith integration test completed!")

if __name__ == "__main__":
    main()
