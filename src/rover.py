import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin, urlparse
import validators
import os
import argparse
from time import time


#Setup the Logger




class ScrapperEngine:
    def __init__(self, 
                 url : str, 
                 html_tags: list = ['img', 'link', 'script'], 
                 timeout: int = 3000,  
                 allowed_requests_responses_codes: list = [200], 
                 *args, 
                 **kwargs
                 ) -> None:
        
        try:
            self.url = self.process_url(url) 
            self.source_code = self.retrieve_source_code(page_url=self.url, 
                                                         timeout=timeout, 
                                                         allowed_requests_responses_codes=allowed_requests_responses_codes)
            
            self.assets = self.retrieve_all_assets_urls(page_url=self.url, source_html=self.source_code, html_tags=html_tags)


        except Exception as e:
            print(f"Encountered {e}")
            exit()

    
    def dump_files(self, output_path:str, ignore_folder_paths : bool = False, *args, **kwargs):
        pass

            
    @staticmethod
    def retrieve_source_code(page_url : str, timeout: int = 3000, allowed_requests_responses_codes : list = [200], verbose=True,*args, **kwargs):
        try:
            response = requests.get(page_url, timeout=timeout)
            if response.status_code in allowed_requests_responses_codes:
                print(f'Successfully retrieved Source Code from {page_url}')
                return response.text
            print(f"Received a blacklisted response code: {response.status_code}")
            exit()
        except requests.RequestException as e:
            print(f"Error during HTTP request: {e}")
        
    
    @staticmethod
    def retrieve_all_assets_urls(page_url: str, source_html, html_tags: list = ['img', 'link', 'script']):
        content = BeautifulSoup(source_html, 'html.parser')
        # Extract and download static assets (images, stylesheets, JavaScript files, etc.)
        try:
            assets_url = {}
            for tag in content.find_all(html_tags):
                src = tag.get('src') or tag.get('href')
                if src:
                    # Convert relative URLs to absolute URLs
                    absolute_url = urljoin(page_url, src)
                    filename = os.path.basename(urlparse(absolute_url).path)
                    assets_url[absolute_url] = filename #Assign Each Assets Url to its filename
                    print(f'\tFile: {filename} detected with URL: {absolute_url}')
            assets_report = f'Detected {len(assets_url.keys())} assets at {page_url}'
            print('#' * len(assets_report))
            print(assets_report)
            print('#' * len(assets_report))
            return assets_url
        except Exception as e:
            print(f"Encoutered {e} while parsing url from Source Code")
            exit()
  
        
    @staticmethod
    def process_url(url : str) -> dict:
        # You can add your own validation logic for the URL here
        # For a simple example, check if the URL starts with 'http' or 'https'
        try:
            if validators.url(url):
                return url
            print(f"Invalid URL Input!: {url}")
            exit()
        except Exception as e:
            print(f"Error detected while processing URL: {e}")
            exit()

    @staticmethod
    def is_valid_output_path(path : str):
        # Check if the path exists and is a directory
        OUTPUT_PATH = Path(path).resolve
        try:
            if OUTPUT_PATH.is_dir():
                return path
            print("Invalid Path Parameter")  
            exit()
        except Exception as e:
            print(f"Invalid Path Error Raise {e} with path: {path}")
            exit()
            
        
if __name__ == "__main__":
    timer = time()
    parser = argparse.ArgumentParser(description='Description of your script.')
    # Add command-line arguments
    parser.add_argument('url', type=str, help='URL to retrieve source code from')
    parser.add_argument('-o','--output-path', type=str, default=".", help='Output Path to dump files')
    parser.add_argument('-p','--ignore_paths', type=bool, default=False, help='Ingore the folder structure of files')
    parser.add_argument('--tags', type=str, default=['img', 'link', 'script'], help='Tags to look for')
    parser.add_argument('-v','--verbose', type=bool, default=True, help='Show verbose output')
    parser.add_argument('-t','--timeout', type=int, default=3000, help='Timeout for the HTTP request')
    parser.add_argument('-s','--allowed-response-codes',type=int, nargs='+', default=[200], help='Allowed Response Codes')

    # Parse the command-line arguments
    args = parser.parse_args()

    assets_obj = ScrapperEngine(url=args.url, html_tags=args.tags,  timeout=args.timeout, allowed_response_codes=args.allowed_response_codes)

    print(f'Duration: {str(time() - timer)} seconds')
