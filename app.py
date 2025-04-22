import csv
import hashlib
import os
import requests
from flask import Flask, request, render_template

app = Flask(__name__)

# Load card list from CSV on startup
CARDS = []
with open("cards.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        CARDS.append({
            "name": row["name"],
            "psa_9_title": row["psa_9_title"],
            "psa_10_title": row["psa_10_title"]
        })

# eBay API credentials (replace with your actual values)
EBAY_APP_ID = "YOUR_EBAY_APP_ID"

def get_average_price(title, condition_filter=None):
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

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"eBay API error: {response.text}")
        return "N/A"

    data = response.json()
    prices = []
    for item in data.get("itemSummaries", []):
        price = item.get("price", {}).get("value")
        if price:
            prices.append(float(price))

    if prices:
        return f"£{sum(prices)/len(prices):.2f}"
    else:
        return "N/A"

@app.route("/")
def index():
    query = request.args.get("q", "").lower()
    results = []

    for card in CARDS:
        if query in card["name"].lower():
            raw_price = get_average_price(card["name"])
            psa_9_price = get_average_price(card["psa_9_title"])
            psa_10_price = get_average_price(card["psa_10_title"])
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
        hashed_value = hashlib.sha256(data_to_hash.encode('utf-8')).hexdigest()
        return {"challengeResponse": hashed_value}
    
    return {"status": "error", "message": "No challenge_code received"}, 400

@app.route("/marketplace-account-deletion-notification", methods=["POST"])
def handle_deletion_notification():
    data = request.get_json()
    print("Received eBay account deletion:", data)
    return {"status": "success", "message": "Notification
