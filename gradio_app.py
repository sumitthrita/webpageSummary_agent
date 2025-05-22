"""
Gradio UI for the website summarization agent.
"""
import gradio as gr
import asyncio
from graph import run_browser_graph

async def summarize_website(url: str) -> str:
    """
    Summarizes the content of a website.
    
    Args:
        url: The URL of the website to summarize
        
    Returns:
        The summary of the website content
    """
    # Check if the URL has a protocol
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"Processing URL: {url}")
    
    try:
        # Run the browser graph
        result = await run_browser_graph(url)
        
        # Check if the summary was generated successfully
        if result["status"] == "success" and result.get("summary"):
            return result["summary"]
        else:
            return f"Error: {result['message']}"
    except Exception as e:
        return f"Error: {str(e)}"

def create_ui():
    """
    Creates the Gradio UI for the website summarization agent.
    """
    # Create the interface
    with gr.Blocks(title="Website Summarization") as demo:
        gr.Markdown("# Website Summarization")
        gr.Markdown("Enter a URL to get a summary of the website content.")
        
        with gr.Row():
            url_input = gr.Textbox(
                label="Website URL",
                placeholder="Enter a website URL (e.g., example.com)",
                scale=4
            )
            submit_button = gr.Button("Summarize", variant="primary", scale=1)
        
        with gr.Row():
            summary_output = gr.Textbox(
                label="Summary",
                placeholder="The summary will appear here...",
                lines=15,
                max_lines=30
            )
        
        # Set up the click event
        submit_button.click(
            fn=lambda url: asyncio.run(summarize_website(url)),
            inputs=url_input,
            outputs=summary_output
        )
        
        # Add examples
        gr.Examples(
            examples=[
                "example.com",
                "wikipedia.org",
                "piramalfinance.com"
            ],
            inputs=url_input
        )
    
    return demo

if __name__ == "__main__":
    # Create and launch the UI
    demo = create_ui()
    demo.launch(share=False)
