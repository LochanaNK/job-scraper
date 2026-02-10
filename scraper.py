import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

#scraper function for rooster.jobs
async def scrape_rooster(search_query):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
    