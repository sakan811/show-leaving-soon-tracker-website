from netflix_scraper import StreamingAvailabilityScraper
import sys
import os

def main():
    # Get the absolute path to the frontend data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Define the base path for saving data
    base_data_path = os.path.join(project_root, 'frontend', 'public', 'data')

    try:
        with StreamingAvailabilityScraper() as scraper:
            # For Thailand
            for service in ["netflix", "hbo"]:
                leaving_titles = scraper.get_leaving_titles(country="th", services=service)
                data_path = os.path.join(base_data_path, f'leaving_titles_th_{service}.json')
                scraper.save_leaving_titles(leaving_titles, data_path)

            # For the United States
            for service in ["netflix", "hbo"]:
                leaving_titles = scraper.get_leaving_titles(country="us", services=service)
                data_path = os.path.join(base_data_path, f'leaving_titles_us_{service}.json')
                scraper.save_leaving_titles(leaving_titles, data_path)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()