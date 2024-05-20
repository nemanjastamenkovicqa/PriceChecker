import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

# Function to get the game name from the Steam website
def get_game_name(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.text.strip().replace(' on Steam', '')
    return None

# Function to update URLs with game names
def update_urls(input_file, output_file, processed_file):
    # Read the list of already processed URLs
    processed_urls = set()
    if os.path.exists(processed_file):
        with open(processed_file, 'r') as f:
            processed_urls = set(line.strip() for line in f.readlines())

    # Read the list of input URLs
    with open(input_file, 'r') as f:
        urls = f.readlines()

    # Open output and processed files for appending
    with open(output_file, 'a') as output_f, open(processed_file, 'a') as processed_f:
        for idx, url in enumerate(urls):
            url = url.strip()
            if url in processed_urls:
                print(f"Skipping already processed URL {idx + 1}/{len(urls)}: {url}")
                continue

            print(f"Processing URL {idx + 1}/{len(urls)}: {url}")
            game_name = get_game_name(url)
            if game_name:
                # Joining URL parts to ensure proper formatting
                updated_url = urljoin(url, game_name.replace(' ', '_') + '/')
                output_f.write(f"{updated_url}\n")
            else:
                output_f.write(f"{url}\n")

            # Log the processed URL
            processed_f.write(f"{url}\n")
            processed_f.flush()  # Ensure the URL is written to the file immediately

# Example usage
input_file = 'listOfGames'  # File containing the list of Steam URLs
output_file = 'updated_steam_urls.txt'  # File to write the updated URLs
processed_file = 'processed_urls.txt'  # File to log the processed URLs

update_urls(input_file, output_file, processed_file)

