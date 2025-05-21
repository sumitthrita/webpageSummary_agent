"""
Browser utilities for opening and controlling a Chromium browser and extracting content.
"""
import os
from typing import Dict, Any
from playwright.async_api import async_playwright
from langchain_community.document_transformers import Html2TextTransformer
from langchain_community.tools.playwright.utils import create_sync_playwright_browser
from langchain_community.tools.playwright.navigate import NavigateTool
from langchain_community.tools.playwright.extract_text import ExtractTextTool
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

async def open_browser_and_navigate(url: str) -> dict:
    """
    Opens a Chromium browser and navigates to the specified URL.
    
    Args:
        url: The URL to navigate to
        
    Returns:
        A dictionary with the status of the operation
    """
    try:
        # Launch the browser in non-headless mode so it's visible
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        
        # Keep the browser open for a while
        await page.wait_for_timeout(10000)  # Keep open for 10 seconds for demo purposes
        
        # Close the browser
        await browser.close()
        await playwright.stop()
        
        return {
            "status": "success",
            "message": f"Successfully opened browser and navigated to {url}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error opening browser: {str(e)}"
        }

async def extract_website_text(url: str) -> Dict[str, Any]:
    """
    Extracts text content from a website using Playwright directly.
    
    Args:
        url: The URL to extract text from
        
    Returns:
        A dictionary with the extracted text and status
    """
    try:
        print(f"Starting text extraction for URL: {url}")
        
        # Launch a headless browser
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Browser launched successfully")
        
        # Navigate to the URL
        await page.goto(url)
        print("Navigated to URL successfully")
        
        # Wait for the page to load completely
        await page.wait_for_load_state("networkidle")
        print("Page loaded completely")
        
        # Extract the text content directly from the page
        text_content = await page.evaluate("() => document.body.innerText")
        print(f"Extracted text length: {len(text_content)}")
        print(f"First 200 characters of extracted text: {text_content[:200]}")
        
        # Close the browser
        await browser.close()
        await playwright.stop()
        print("Browser closed successfully")
        
        if not text_content or len(text_content.strip()) == 0:
            print("WARNING: Extracted text is empty!")
            return {
                "status": "error",
                "text_content": "",
                "message": "Failed to extract text: Empty content"
            }
        
        return {
            "status": "success",
            "text_content": text_content,
            "message": "Successfully extracted text from website"
        }
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        return {
            "status": "error",
            "text_content": "",
            "message": f"Error extracting text: {str(e)}"
        }

async def generate_summary(text: str) -> Dict[str, Any]:
    """
    Generates a summary of the provided text using Claude.
    
    Args:
        text: The text to summarize
        
    Returns:
        A dictionary with the summary and status
    """
    try:
        print(f"Starting summary generation for text of length: {len(text)}")
        print(f"First 200 characters of text to summarize: {text[:200]}")
        
        if not text or len(text.strip()) == 0:
            print("WARNING: Text to summarize is empty!")
            return {
                "status": "error",
                "summary": "No content was provided for summarization.",
                "message": "Failed to generate summary: Empty content"
            }
        
        # Truncate text if it's too long (Claude has context limits)
        max_length = 100000  # Adjust based on Claude's limits
        truncated_text = text[:max_length] if len(text) > max_length else text
        print(f"Text truncated to {len(truncated_text)} characters")
        
        # Create the prompt for Claude
        prompt = f"""
        Please provide a comprehensive summary of the following website content. 
        Focus on the main topics, key information, and overall purpose of the website.
        
        Website Content:
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
