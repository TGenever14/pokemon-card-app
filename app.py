from flask import Flask, render_template
import csv
import os
import requests
import time
from datetime import datetime, timedelta

app = Flask(__name__)

# Cache dictionary
PRICE_CACHE = {}

# Read card data from CSV
def read_csv():
    cards = []
    with open("cards.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cards.append({
                "name": row["Name"],
                "psa10_query": row["PSA_10_Query"],
                "raw_query": row["Raw_Query"]
            })
    return cards

# Function to get average price from eBay with caching and rate limit handling
def get_average_price(title):
    if title in PRICE_CACHE:
        cached_price, timestamp = PRICE_CACHE[title]
        if datetime.now() - timestamp < timedelta(hours=48):  # Cache for 48 hours
            return cached_price

    url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
    headers = {
        "Authorization": f"Bearer {os.getenv('EBAY_BEARER_TOKEN')}",
        "X-EBAY-C-ENDUSERCTX": "contextualLocation=country=GB",
    }
    params = {
        "q": title,
        "filter": "buyingOptions:{FIXED_PRICE},priceCurrency:GBP,conditions:{USED},itemLocationCountry:GB",
        "limit": "10",
        "sort": "-price",
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        time.sleep(1)  # Throttle a bit between requests

        if response.status_code == 429 or response.status_code == 2001:
            print("Rate limit hit. Waiting 60s before retry...")
            time.sleep(60)
            return get_average_price(title)

        if response.status_code != 200:
            print(f"eBay API error: {response.text}")
            return "N/A"

        data = response.json()
        prices = [
            float(item["price"]["value"])
            for item in data.get("itemSummaries", [])
            if "price" in item and "value" in item["price"]
        ]

        if prices:
            average = f"£{sum(prices) / len(prices):.2f}"
        else:
            average = "N/A"

        PRICE_CACHE[title] = (average, datetime.now())
        return average

    except Exception as e:
        print(f"Error fetching price for '{title}': {e}")
        return "N/A"

@app.route("/")
def index():
    cards = read_csv()
    for card in cards:
        card["psa10_price"] = get_average_price(card["psa10_query"])
        card["raw_price"] = get_average_price(card["raw_query"])
    return render_template("index.html", cards=cards)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
