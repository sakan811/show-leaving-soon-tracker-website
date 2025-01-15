import requests
import logging
import json
import os
import datetime

from dotenv import load_dotenv

load_dotenv()

class StreamingAvailabilityScraper:
    """
    A class to scrape leaving titles information from Streaming Availability API
    """
    
    def __init__(self):
        """
        Initialize the Streaming Availability scraper
        """

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        # Return the instance itself when entering the context
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Handle cleanup if necessary (currently, there's nothing to clean up)
        pass
    
    def get_leaving_titles(self):
        """
        Gets all leaving dates and their corresponding show titles from Streaming Availability API.
            
        Returns:
            list: List of tuples containing leaving date and corresponding show titles
        """
        try:
            url = "https://streaming-availability.p.rapidapi.com/leaving"
            
            querystring = {"output_language":"en","target_type":"show","services":"netflix","country":"th"}

            headers = {
                "x-rapidapi-key": os.getenv("API_KEY"),
                "x-rapidapi-host": "streaming-availability.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            
            leaving_titles = []
            for item in data.get('result', []):
                show = item.get('show', {})
                title = show.get('title')
                
                # Get streaming info for Thailand (th) region
                streaming_info = show.get('streamingInfo', {}).get('th', [])
                for info in streaming_info:
                    if info.get('service') == 'netflix' and 'leaving' in info:
                        leaving_date = info['leaving']
                        
                        # Convert timestamp to formatted date
                        date_time = datetime.datetime.fromtimestamp(leaving_date)
                        formatted_date = date_time.strftime('%Y-%m-%d')
                        
                        leaving_titles.append((formatted_date, title))
            
            self.logger.info(f"Successfully retrieved {len(leaving_titles)} leaving titles")
            return leaving_titles
            
        except Exception as e:
            self.logger.error(f"Error getting leaving titles from the API: {str(e)}")
            return []

    def save_leaving_titles(self, leaving_data, output_path):
        """
        Save leaving titles data to JSON file.
        
        Args:
            leaving_data (list): List of tuples containing (date, title)
            output_path (str): Path to save JSON file
        """
        try:
            # Convert list of tuples to structured dictionary
            formatted_data = {}
            for date, title in leaving_data:
                if date not in formatted_data:
                    formatted_data[date] = []
                formatted_data[date].append(title)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save to JSON file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(formatted_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Successfully saved leaving titles to {output_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving leaving titles: {str(e)}")
