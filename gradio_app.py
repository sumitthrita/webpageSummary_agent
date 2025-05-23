"""
Gradio UI for the website and PDF summarization agent.
"""
import gradio as gr
import asyncio
import os
import tempfile
from graph import run_browser_graph
from pdf_utils import extract_text_from_pdf, generate_pdf_summary

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

async def summarize_pdf(pdf_file) -> str:
    """
    Summarizes the content of a PDF file.
    
    Args:
        pdf_file: The uploaded PDF file
        
    Returns:
        The summary of the PDF content
    """
    if pdf_file is None:
        return "Error: No PDF file uploaded."
    
    try:
        # Create a temporary file to save the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_path = temp_file.name
            # Write the uploaded file to the temporary file
            temp_file.write(pdf_file)
        
        print(f"PDF saved to temporary file: {temp_path}")
        
        # Extract text from the PDF
        text_content = extract_text_from_pdf(temp_path)
        
        # Clean up the temporary file
        os.unlink(temp_path)
        
        if not text_content:
            return "Error: Could not extract text from the PDF file."
        
        # Generate a summary of the PDF content
        result = await generate_pdf_summary(text_content)
        
        # Check if the summary was generated successfully
        if result["status"] == "success" and result.get("summary"):
            return result["summary"]
        else:
            return f"Error: {result['message']}"
    except Exception as e:
        # Clean up the temporary file if it exists
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.unlink(temp_path)
        return f"Error: {str(e)}"

def create_ui():
    """
    Creates the Gradio UI for the website and PDF summarization agent.
    """
    # Create the interface
    with gr.Blocks(title="Content Summarization") as demo:
        gr.Markdown("# Content Summarization")
        gr.Markdown("Enter a URL or upload a PDF file to get a summary of the content.")
        
        with gr.Tabs():
            with gr.TabItem("Website Summarization"):
                with gr.Row():
                    url_input = gr.Textbox(
                        label="Website URL",
                        placeholder="Enter a website URL (e.g., example.com)",
                        scale=4
                    )
                    website_submit_button = gr.Button("Summarize Website", variant="primary", scale=1)
                
                # Add examples for websites
                gr.Examples(
                    examples=[
                        "example.com",
                        "wikipedia.org",
                        "piramalfinance.com"
                    ],
                    inputs=url_input
                )
            
            with gr.TabItem("PDF Summarization"):
                with gr.Row():
                    pdf_input = gr.File(
                        label="Upload PDF",
                        file_types=[".pdf"],
                        type="binary"
                    )
                    pdf_submit_button = gr.Button("Summarize PDF", variant="primary")
        
        with gr.Row():
            summary_output = gr.Textbox(
                label="Summary",
                placeholder="The summary will appear here...",
                lines=15,
                max_lines=30
            )
        
        # Set up the click events
        website_submit_button.click(
            fn=lambda url: asyncio.run(summarize_website(url)),
            inputs=url_input,
            outputs=summary_output
        )
        
        pdf_submit_button.click(
            fn=lambda pdf: asyncio.run(summarize_pdf(pdf)),
            inputs=pdf_input,
            outputs=summary_output
        )
    
    return demo

if __name__ == "__main__":
    # Create and launch the UI
    demo = create_ui()
    demo.launch(share=False)
