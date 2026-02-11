import asyncio
from playwright.async_api import async_playwright


#scraper function for rooster.jobs
async def scrape_rooster(search_query):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        page = await context.new_page()
        
        
        url = f"https://rooster.jobs/?query={search_query}&limit=50&page=1"
        print(f"Navigating to {url}")
        
        try:
            await page.goto(url, wait_until="domcontentloaded")
        
            job_selector = "div.job-item"
            await page.wait_for_selector(job_selector,timeout=15000)
            
            await asyncio.sleep(1)
            
            jobs = await page.query_selector_all(job_selector)
            results = []
            
            for job in jobs:
                title = "n/a"
                company = "n/a"
                full_link = "n/a"
                raw_date = "n/a"
                
                try:
                    title_el = await job.query_selector("h5.job-title-h5")
                    company_el = await job.query_selector("button.ant-btn")
                    link_el = await job.query_selector("a.job-title")
                    
                    try:
                        date_el = await job.locator("div.posted-on-label span").inner_text()
                        raw_date = date_el.split("on")[-1].strip()
                    except Exception as e:
                        raw_date = "n/a"
                    
                    if title_el:
                        title = await title_el.inner_text()
                    if company_el:
                        company = await company_el.inner_text()
                    if link_el:
                        raw_link = await link_el.get_attribute("href")
                        if raw_link:
                            full_link = f"https://rooster.jobs{raw_link}" if raw_link.startswith("/") else raw_link
                    
                    
                    is_intern = "intern" in title.lower()
                    is_2026 = "26" in raw_date or "2026" in raw_date
                    
                    if title != "n/a" and is_intern and is_2026:
                        results.append({
                        "title": title.strip(),
                        "company": company.strip(),
                        "link": full_link,
                        "date_posted": raw_date
                    })
                except Exception as e:
                    print(f"Error extracting job details: {e}")
                    continue
            
            await browser.close()
            return results
        
        except Exception as e:
            print("an error occurred:",e)
            await browser.close()
            return []

if __name__ == "__main__":
    search_query = "software engineer intern"
    jobs_found = asyncio.run(scrape_rooster(search_query))
    
    for job in jobs_found:
        print(f"Title: {job['title']}, Company: {job['company']}, Link: {job['link']}, Date Posted: {job['date_posted']}")
        
    