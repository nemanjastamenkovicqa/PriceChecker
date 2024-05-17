import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
def update_urls(input_file, output_file):
    with open(input_file, 'r') as f:
        urls = f.readlines()

    with open(output_file, 'w') as f:
        for idx, url in enumerate(urls):
            url = url.strip()
            print(f"Processing URL {idx + 1}/{len(urls)}: {url}")
            game_name = get_game_name(url)
            if game_name:
                # Joining URL parts to ensure proper formatting
                updated_url = urljoin(url, game_name.replace(' ', '_') + '/')
                f.write(f"{updated_url}\n")
            else:
                f.write(f"{url}\n")

# Example usage
input_file = 'listOfGames'  # File containing the list of Steam URLs
output_file = 'updated_steam_urls.txt'  # File to write the updated URLs
update_urls(input_file, output_file)

