import csv
import hashlib
import os
import time
import requests
from flask import Flask, request, render_template

app = Flask(__name__)

# Load card list from CSV on startup
CARDS = []
with open("cards.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        CARDS.append({
            "name": row["Name"],
            "psa_9_query": row["PSA_9_Query"],
            "psa_10_query": row["PSA_10_Query"],
            "raw_query": row["Raw_Query"],
        })

# eBay API credentials
EBAY_APP_ID = "YOUR_EBAY_APP_ID"

# Simple in-memory cache for prices
PRICE_CACHE = {}

def get_average_price(title, condition_filter=None):
    # Check cache first
    if title in PRICE_CACHE:
        return PRICE_CACHE[title]

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
        time.sleep(1)  # Throttle to 1 request per second

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

        # Cache the result
        PRICE_CACHE[title] = average
        return average

    except Exception as e:
        print(f"Error fetching price for '{title}': {e}")
        return "N/A"

@app.route("/")
def index():
    query = request.args.get("q", "").lower()
    results = []

    for card in CARDS:
        if query in card["name"].lower():
            raw_price = "£0.00"
            psa_9_price = "£0.00"
            psa_10_price = "£0.00"
            results.append({
                "name": card["name"],
                "raw": raw_price,
                "psa_9": psa_9_price,
                "psa_10": psa_10_price,
            })

    return render_template("index.html", results=results, query=query)

@app.route("/marketplace-deletion-verification", methods=["GET"])
def verify_token():
    challenge_code = request.args.get("challenge_code")
    token_from_ebay = request.args.get("token")
    EXPECTED_TOKEN = os.getenv("EBAY_VERIFICATION_TOKEN")
    EXPECTED_ENDPOINT = "https://pokemon-card-app.onrender.com/marketplace-deletion-verification"

    if token_from_ebay != EXPECTED_TOKEN:
        return {"status": "error", "message": "Invalid token"}, 400

    if challenge_code:
        data_to_hash = challenge_code + EXPECTED_TOKEN + EXPECTED_ENDPOINT
        hashed_value = hashlib.sha256(data_to_hash.encode()).hexdigest()
        return {"status": "success", "hashed_value": hashed_value}, 200

    return {"status": "error", "message": "Challenge code missing"}, 400

# Ensure the app binds to the correct port when deployed on Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
