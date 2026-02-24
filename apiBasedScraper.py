import requests
import json
from bs4 import BeautifulSoup



#Rooster scraper

def api_rooster(search_query):
    
    
    api_url = "https://api.rooster.jobs/jobSearch/jobs/search"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://rooster.jobs/jobs",
    }
    
    payload = {
       "query": [search_query],
        "limit": 50,
        "page": 1,
        "filters": {}
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
    
        print(f"DEBUG: Status {response.status_code}")
    
        if response.status_code in  [200, 201]:
            data = response.json()
            
            print(f"DEBUG: Data keys found: {list(data.keys())}")
            jobs = data.get("body", {}).get("data", [])
            
            if not jobs and isinstance(data, list):
                jobs = data
            
            internships_2026 = []
            for job in jobs:

                created_at = job.get('updated_at', '')
                job_title = job.get('title','').lower()
                
                if ("2026" in created_at or "26" in created_at) and "intern" in job_title:
                    internships_2026.append({
                        "title": job.get('title'),
                        "company": job.get('company_name'),
                        "location": job.get('location'),
                        "created_at": created_at,
                        "link": f"https://rooster.jobs/jobs/{job.get('id')}",
                        "source": "rooster"
                    })
            return internships_2026
        return []
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return []


#Jobhunder scraper

def api_jobhunder(search_query):
    formatted_query = search_query.strip().replace(' ', '+')
    api_url = f"https://www.jobhunder.com/search?q={formatted_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = []
        
        articles = soup.find_all('article', class_='blog-post')
        
        for article in articles:

            title_h2 = article.find('h2', class_='entry-title')
            link_tag = title_h2.find('a') if title_h2 else None
            
            company_tag = article.find('span', class_='label-news-flex')
            
            date_tag = article.find('span', class_='post-date')

            if link_tag:
                if "2026" in date_tag.text or "26" in date_tag.text:
                    if "intern" in title_h2.text.lower():
                        jobs.append({
                            "title": link_tag.get_text(strip=True),
                            "company": company_tag.get_text(strip=True) if company_tag else "Jobhunder",
                            "location": "Sri Lanka",
                            "created_at": date_tag.get_text(strip=True) if date_tag else "Recent",
                            "link": link_tag['href'],
                            "source": "jobhunder"
                        })
        return jobs
    except Exception as e:
        print(f"Jobhunder Scraping Error: {e}")
        return []

def save_to_json(jobs, filename="internships_2026.json"):
    if not jobs:
        print("No jobs found to save.")
        return

    # 'w' mode opens the file for writing (overwrites existing)
    with open(filename, 'w', encoding='utf-8') as f:
        # indent=4 makes the file human-readable
        # ensure_ascii=False keeps special characters (like symbols or emojis) intact
        json.dump(jobs, f, indent=4, ensure_ascii=False)
    
    print(f"Successfully saved {len(jobs)} jobs to {filename}")

