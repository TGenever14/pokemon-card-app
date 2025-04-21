from flask import Flask, render_template
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

if __name__ == "__main__":
    app.run(debug=True)