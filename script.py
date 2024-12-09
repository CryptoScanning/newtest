import time
import requests
import threading
from flask import Flask

# Flask setup for keep-alive
app = Flask(__name__)

@app.route("/")
def home():
    return "Server is running!"

def start_server():
    app.run(host="0.0.0.0", port=5000)

def keep_alive():
    while True:
        try:
            # Send a ping request to the server's local URL
            ping_response = requests.get("https://replit.com/@ltcbot/newtest)
            print(f"Keep-alive ping response: {ping_response.status_code}")
        except Exception as e:
            print(f"Keep-alive ping failed: {e}")
        time.sleep(600)  # Ping every 10 minutes

# Litecoin price monitoring
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

def monitor_litecoin():
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

# Run both the Flask server and Litecoin monitoring
if __name__ == "__main__":
    # Start Flask server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    # Start the keep-alive ping mechanism in another thread
    keep_alive_thread = threading.Thread(target=keep_alive)
    keep_alive_thread.daemon = True
    keep_alive_thread.start()

    # Start monitoring Litecoin price
    monitor_litecoin()
