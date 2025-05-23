"""
Utility functions for working with PDF files.
"""
import os
import PyPDF2
from typing import Dict, Any
import anthropic

# Load the Anthropic API key from environment variables
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text content from a PDF file.
    
    Args:
        pdf_path: The path to the PDF file
        
    Returns:
        The extracted text content
    """
    try:
        print(f"Extracting text from PDF: {pdf_path}")
        
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Get the number of pages
            num_pages = len(pdf_reader.pages)
            print(f"PDF has {num_pages} pages")
            
            # Extract text from each page
            text_content = ""
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text() + "\n\n"
            
            print(f"Extracted text length: {len(text_content)}")
            if text_content:
                print(f"First 200 characters of extracted text: {text_content[:200]}")
            
            return text_content
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return ""

async def generate_pdf_summary(text: str) -> Dict[str, Any]:
    """
    Generates a summary of the provided PDF text using Claude.
    
    Args:
        text: The text to summarize
        
    Returns:
        A dictionary with the summary and status
    """
    try:
        print(f"Starting summary generation for PDF text of length: {len(text)}")
        print(f"First 200 characters of text to summarize: {text[:200]}")
        
        if not text or len(text.strip()) == 0:
            print("WARNING: Text to summarize is empty!")
            return {
                "status": "error",
                "summary": "No content was extracted from the PDF for summarization.",
                "message": "Failed to generate summary: Empty content"
            }
        
        # Truncate text if it's too long (Claude has context limits)
        max_length = 100000  # Adjust based on Claude's limits
        truncated_text = text[:max_length] if len(text) > max_length else text
        print(f"Text truncated to {len(truncated_text)} characters")
        
        # Create the prompt for Claude
        prompt = f"""
        Please provide a comprehensive summary of the following PDF document content. 
        Focus on the main topics, key information, and overall purpose of the document.
        
        Document Content:
        {truncated_text}
        
        Summary:
        """
        
        print("Sending request to Claude API...")
        
        # Generate the summary using Claude
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0.2,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the summary from the response
        summary = response.content[0].text
        print(f"Received summary of length: {len(summary)}")
        print(f"First 200 characters of summary: {summary[:200]}")
        
        return {
            "status": "success",
            "summary": summary,
            "message": "Successfully generated summary"
        }
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return {
            "status": "error",
            "summary": "",
            "message": f"Error generating summary: {str(e)}"
        }
