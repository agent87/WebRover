import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlsplit, urlunparse
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
                 ignore_domains: list = [],
                 enforce_base_url: bool = False,
                 *args, 
                 **kwargs
                 ) -> None:
        
        try:
            
            if not validators.url(url):
                print(f"Invalid URL Input!: {url}")
                raise ValueError("Invalid URL")
 
            self.base_url = url
            self.source_page = self.retrieve_content(page_url=self.base_url, timeout=timeout,allowed_requests_responses_codes=allowed_requests_responses_codes).text
            self.urls = self.retrieve_urls(page_url=self.base_url, source_html=self.source_page, html_tags=html_tags, enforce_base_url=True)


        except Exception as e:
            print(f"Encountered {e}")
            exit()


    def export(self, output_path:str = 'output', ignore_folder_paths : bool = False, *args, **kwargs):
        for url, description in self.urls.items():
            try:
                response = requests.get(url)
                if response.status_code == 200:
                        OUTPUT_PATH=Path(output_path + str(Path(description['path']).parent)).resolve()
                        OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
                        with open(OUTPUT_PATH / description['filename'], 'wb') as file:
                            file.write(response.content)
                        print(f'Successfully retrieved file: {description['filename']} with url: {url}')
                else:
                        print(f"Unable to retrieve file: {description['filename']} with Url:{url} -> Error")
                        pass


                    # # Save the content to the local file
                    # with open(local_path, "wb") as file:
                    #     file.write(response.content)

                    # downloaded_files[file_name] = local_path
                    # print(f"Downloaded: {file_name}")
            except requests.exceptions.RequestException as e:
                    print(f"Error downloading {description['filename']}: {e}")

    def visualize(self):
        pass

    @staticmethod
    def retrieve_content(page_url : str, timeout: int = 3000, allowed_requests_responses_codes : list = [200], verbose=True,*args, **kwargs):
        try:
            response = requests.get(page_url, timeout=timeout)
            if response.status_code in allowed_requests_responses_codes:
                print(f'Successfully Retrieved Content from {page_url}')
                return response
            print(f"Received a blacklisted response code: {response.status_code}")
            exit()
        except requests.RequestException as e:
            print(f"Error during HTTP request: {e}")
        
    
    @staticmethod
    def retrieve_urls(page_url: str, source_html, html_tags: list = ['img', 'link', 'script'], enforce_base_url: bool = False):
        content = BeautifulSoup(source_html, 'html.parser')
        # Extract and download static assets (images, stylesheets, JavaScript files, etc.)
        try:
            urls = {}
            for tag in content.find_all(html_tags):
                src = tag.get('src') or tag.get('href')
                if src:
                    # Convert relative URLs to absolute URLs
                    file_url = urljoin(page_url, src)
                    file_url_obj = urlparse(file_url)
                    parsed_url = urlparse(urljoin(page_url, src))
                    if enforce_base_url:
                        if file_url_obj.hostname == urlsplit(page_url).hostname:
                            urls[file_url] = ScrapperEngine.process_url(file_url)
                            print(f'\tFile: {os.path.basename(file_url)} detected with URL: {file_url}')
                    else:
                        filename = os.path.basename(parsed_url.path)
                        urls[parsed_url] = filename #Assign Each Assets Url to its filename
                        print(f'\tFile: {filename} detected with URL: {parsed_url}')

            assets_report = f'Detected {len(urls.keys())} assets at {page_url}'
            print('#' * len(assets_report))
            print(assets_report)
            print('#' * len(assets_report))
            return urls
        except Exception as e:
            print(f"Encoutered {e} while parsing url from Source Code")
            exit()
  
        
    @staticmethod
    def process_url(url : str) -> dict:
        # You can add your own validation logic for the URL here
        # For a simple example, check if the URL starts with 'http' or 'https'
        
        try:
            if not validators.url(url):
                print(f"Invalid URL Input!: {url}")
                raise ValueError("Invalid URL")
            parsed_url = urlparse(url)
            return {
                'domain': parsed_url.hostname,
                'path': parsed_url.path,
                'filename' : os.path.basename(urlparse(url).path),
                'extension' :  os.path.splitext(url)[1]
            }
        except Exception as e:
            print(f"Error detected while processing URL: {e}")
            exit()

    @staticmethod
    def validate_file_path(path : str) -> str:
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

    assets_obj.export('static')

    print(f'Duration: {str(time() - timer)} seconds')
