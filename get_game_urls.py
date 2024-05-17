import requests
from bs4 import BeautifulSoup

def get_all_game_urls():
    # Steam API endpoint for getting app list
    app_list_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

    try:
        # Fetch the app list from Steam API
        response = requests.get(app_list_url)
        data = response.json()

        # Extract app IDs
        app_ids = [app['appid'] for app in data['applist']['apps']]

        # Construct game URLs
        game_urls = [f"https://store.steampowered.com/app/{app_id}/" for app_id in app_ids]

        return game_urls

    except Exception as e:
        print("Error fetching game URLs:", e)
        return []

def get_game_name(url):
    try:
        # Fetch HTML content of the game page
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the game name
        game_name = soup.find('div', class_='apphub_AppName').text.strip()

        return game_name

    except Exception as e:
        print("Error fetching game name:", e)
        return None

def save_to_file(game_names_and_urls):
    try:
        with open("listOfGames.txt", "w") as file:
            for game_name, game_url in game_names_and_urls:
                file.write(f"{game_name}: {game_url}\n")
        print("Game names and URLs saved to listOfGames.txt")
    except Exception as e:
        print("Error saving to file:", e)

# Example usage
if __name__ == "__main__":
    game_urls = get_all_game_urls()
    game_names_and_urls = [(get_game_name(url), url) for url in game_urls]
    save_to_file(game_names_and_urls)

