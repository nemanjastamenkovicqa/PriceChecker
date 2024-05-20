#!/bin/bash

# Define color codes
orange='\033[0;33m'
reset='\033[0m'

# Function to search for URLs and process them
search_urls() {
    # Prompt the user to enter a keyword
    read -p "Enter the keyword to search for: " keyword

    # Search for the keyword in the updated_steam_urls.txt file and process matching URLs
    grep -i "$keyword" updated_steam_urls.txt | while IFS= read -r line; do
        # Extract the part after 'app/' from the URL
        link_part=$(echo "$line" | sed 's|.*app/||')

        # Fetch the HTML content of the webpage and save it to a variable
        webpage=$(curl -s "$line")

        # Check if the game is on discount
        discount_line=$(echo "$webpage" | grep 'class="discount_block game_purchase_discount" data-price-final="')
        if [ -n "$discount_line" ]; then
            # Extract the discounted price
            price=$(echo "$discount_line" | grep -oP 'class="discount_block game_purchase_discount" data-price-final="\K[0-9,]+')
        else
            # Extract the regular price
            price_line=$(echo "$webpage" | grep 'div class="game_purchase_price price" data-price-final="')
            price=$(echo "$price_line" | grep -oP 'div class="game_purchase_price price" data-price-final="\K[0-9,]+')
        fi

        # Remove commas and convert to a number
        numeric_price=$(echo "$price" | tr -d ',')

        # Print the current price along with the game link part in orange
        echo -e "The current price of ${orange}$link_part${reset} is €$price"
    done
}

# Main loop
while true; do
    # Run the search function
    search_urls

    # Ask if the user wants to run the script again or quit
    read -p "Do you want to run the script again? (yes/no): " choice
    case $choice in
        [Yy][Ee][Ss]|[Yy])
            continue
            ;;
        [Nn][Oo]|[Nn])
            echo "Exiting..."
            break
            ;;
        *)
            echo "Invalid choice. Please enter 'yes' or 'no'."
            ;;
    esac
done

