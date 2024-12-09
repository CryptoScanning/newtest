import time
import requests

def fetch_litecoin_price():
    try:
        # Using the specified CoinGecko API URL for Litecoin price
        url = "https://api.coingecko.com/api/v3/coins/litecoin?tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        data = response.json()
        # Extract the USD price from the nested structure
        price = data["market_data"]["current_price"]["usd"]
        return price
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching Litecoin price: {e}")
        return None

def main():
    print("Monitoring Litecoin price. Press Ctrl+C to stop.")
    old_price = None  # Initialize old price as None
    
    while True:
        current_price = fetch_litecoin_price()
        if current_price is not None:
            if old_price is None:  # First fetch, no previous price to compare
                print(f"The current price of Litecoin is: ${current_price}")
            elif current_price != old_price:  # Print only if price changes
                print(f"The price of Litecoin has changed from ${old_price} to ${current_price}")
            old_price = current_price  # Update old price with the current one
        else:
            print("Could not retrieve the price. Retrying...")
        
        time.sleep(10)  # Wait for 10 seconds before the next request

main()
