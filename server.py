from fastapi import FastAPI
from apiBasedScraper import api_rooster, api_jobhunder
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from importlib.metadata import version

server = FastAPI()

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@server.get('/scrape')
async def run_scraper(query: str):
    results = api_rooster(query)
    results.extend(api_jobhunder(query))
    return {"results" : results}


print(f"FastAPI Version: {version('fastapi')}")

print(f"Uvicorn Version: {version('uvicorn')}")
print(f"Requests Version: {version('requests')}")



if __name__ == "__main__":
    uvicorn.run(server, host='0.0.0.0', port=8000)
    