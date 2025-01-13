from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import json
import os

class NetflixScraper:
    """
    A class to scrape movie information from Netflix
    
    Attributes:
        driver: Selenium WebDriver instance
    """
    
    def __init__(self, headless: bool = True):
        """
        Initialize the Netflix scraper
        
        Args:
            headless: Whether to run browser in headless mode
        """
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=options)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def get_leaving_dates_and_titles(self, url):
        """
        Gets all leaving dates and their corresponding show titles from Netflix Tudum page.
        
        Args:
            url (str): The URL of the Netflix Tudum leaving soon page
            
        Returns:
            list: List of tuples containing leaving date and corresponding show titles
        """
        self.driver.get(url)
        
        # Wait for the content to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-sel='article-content']"))
        )
        
        try:
            # Find all h3 elements within article-content
            content = self.driver.find_elements(
                By.CSS_SELECTOR, 
                "div[data-sel='article-content'] h3[data-sel='heading']"
            )
            
            leaving_data = []
            current_date = None
            
            for element in content:
                if 'css-1i31ble' in element.get_attribute('class'):
                    # This is a leaving date
                    current_date = element.text.strip()
                elif 'css-4maxu3' in element.get_attribute('class'):
                    # This is a show title
                    if current_date:
                        leaving_data.append((current_date, element.text.strip()))
            
            return leaving_data
            
        except Exception as e:
            self.logger.error(f"Error finding leaving dates and titles: {str(e)}")
            return []

    def close(self):
        """Close the browser and cleanup"""
        if self.driver:
            self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

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
