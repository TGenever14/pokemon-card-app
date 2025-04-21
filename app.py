from flask import Flask, render_template, request, jsonify
import requests
import statistics

app = Flask(__name__)

# Your eBay App ID
APP_ID = "TomGenev-CardValu-PRD-6261c5cd3-e868ed16"

# Example cards
cards = [
    {"name": "Charizard Base Set", "search_raw": "Charizard Base Set -PSA -BGS -CGC", "search_psa": "Charizard Base Set PSA 10"},
    {"name": "Pikachu Base Set", "search_raw": "Pikachu Base Set -PSA -BGS -CGC", "search_psa": "Pikachu Base Set PSA 10"},
]

# This is your eBay verification token
EXPECTED_TOKEN = "mCk87t3oXZQfEpYs2RuJpGbvTnqW9cUL1DJHMe5sKFiAWla0xBYzNh4g"

def get_average_price(query):
    # Dummy data for now
    prices = [12.99, 15.49, 13.75, 11.30, 14.00]
    avg_price = round(statistics.mean(prices), 2)
    return avg_price

@app.route("/")
def index():
    results = []
    for card in cards:
        raw_price = get_average_price(card["search_raw"])
        psa_price = get_average_price(card["search_psa"])
        results.append({
            "name": card["name"],
            "raw": f"£{raw_price}",
            "psa10": f"£{psa_price}"
        })
    return render_template("index.html", cards=results)

@app.route("/marketplace-deletion-verification", methods=["GET"])
def verify_token():
    token_from_ebay = request.args.get("token")
    if token_from_ebay == EXPECTED_TOKEN:
        return jsonify({"status": "success", "message": "Token verified successfully"})
    else:
        return jsonify({"status": "error", "message": "Invalid token"}), 400

@app.route("/debug")
def debug():
    return jsonify({"status": "debug endpoint is working"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
