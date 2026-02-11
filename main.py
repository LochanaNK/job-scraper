from apiBasedScraper import api_rooster, save_to_json

def main():
    
    search_query = input("Enter job search query: ")
    results = api_rooster(search_query)
    save_to_json(results)
    

    
if __name__ == "__main__":
    main()