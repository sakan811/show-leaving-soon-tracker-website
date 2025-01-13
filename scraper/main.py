from netflix_scraper import NetflixScraper
import sys
import os

def main():
    url = "https://www.netflix.com/tudum/articles/whats-leaving-netflix"
    
    # Get the absolute path to the frontend data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_path = os.path.join(project_root, 'frontend', 'public', 'data', 'leaving_titles_jan_2025.json')
    
    try:
        with NetflixScraper(headless=True) as scraper:
            leaving_titles = scraper.get_leaving_dates_and_titles(url)
            scraper.save_leaving_titles(leaving_titles, data_path)
                
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()