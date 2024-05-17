#!/bin/bash

# Define color codes
orange='\033[0;33m'
reset='\033[0m'

# Check if listOfGames file exists
if [ ! -f "listOfGames" ]; then
    echo "Error: listOfGames file not found."
    exit 1
fi

# Read each URL from the listOfGames file and process it
while IFS= read -r url; do
    # Extract the specific part of the link from the URL
    link_part=$(echo "$url" | sed 's|https://store.steampowered.com/||')

    # Fetch the HTML content of the webpage and save it to a file
    curl -s "$url" > webpage.html

    # Check if the game is on discount
    discount_line=$(grep 'class="discount_block game_purchase_discount" data-price-final="' webpage.html)
    if [ -n "$discount_line" ]; then
        # Extract the discounted price
        price=$(echo "$discount_line" | grep -oP 'class="discount_block game_purchase_discount" data-price-final="\K[0-9,]+')
    else
        # Extract the regular price
        price_line=$(grep 'div class="game_purchase_price price" data-price-final="' webpage.html)
        price=$(echo "$price_line" | grep -oP 'div class="game_purchase_price price" data-price-final="\K[0-9,]+')
    fi

    # Remove commas and convert to a number
    numeric_price=$(echo "$price" | tr -d ',')

    # Print the current price along with the game link part in orange
    echo -e "The current price of ${orange}$link_part${reset} is €$price"

done < "listOfGames"

