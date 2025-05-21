"""
Browser utilities for opening and controlling a Chromium browser.
"""
from playwright.async_api import async_playwright

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
        await page.wait_for_timeout(30000)  # Keep open for 30 seconds for demo purposes
        
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
