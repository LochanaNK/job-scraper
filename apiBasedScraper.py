import requests
import json

def api_job_scraper():
    api_url = "https://api.rooster.jobs/jobSearch/jobs/search"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://rooster.jobs/jobs",
    }
    
    payload = {
       "query": ["software engineer intern"],
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
                        "link": f"https://rooster.jobs/job/{job.get('id')}"
                    })
            return internships_2026
        return []
        
    except Exception as e:
        print(f"Error occurred: {e}")
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


    
if __name__ == "__main__":
    results = api_job_scraper()
    save_to_json(results)
    print(f"✅ Found {len(results)} internships from 2026:")
    for res in results:
        print(f" - {res['title']} at {res['company']} ({res['location']}) ({res['link']}) (Posted: {res.get('created_at', 'N/A')})")