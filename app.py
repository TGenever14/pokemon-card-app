import hashlib
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Enable logging
logging.basicConfig(level=logging.INFO)

# Your eBay verification token
EXPECTED_TOKEN = "mCk87t3oXZQfEpYs2RuJpGbvTnqW9cUL1DJHMe5sKFiAWla0xBYzNh4g"
# Your callback URL (must match what eBay has)
EXPECTED_ENDPOINT = "https://pokemon-card-app.onrender.com/marketplace-deletion-verification"

@app.route("/")
def home():
    return "Service running!"

# GET request handler for eBay verification
@app.route("/marketplace-deletion-verification", methods=["GET"])
def verify_token():
    challenge_code = request.args.get("challenge_code")
    token_from_ebay = request.args.get("token")
    
    app.logger.info("Received GET request with args: %s", request.args)

    if token_from_ebay != EXPECTED_TOKEN:
        return jsonify({"status": "error", "message": "Invalid token"}), 400

    if challenge_code:
        data_to_hash = challenge_code + EXPECTED_TOKEN + EXPECTED_ENDPOINT
        hashed_value = hashlib.sha256(data_to_hash.encode('utf-8')).hexdigest()
        return jsonify({"challengeResponse": hashed_value})

    return jsonify({"status": "error", "message": "No challenge_code received"}), 400

# POST request handler for deletion notifications
@app.route("/marketplace-deletion-verification", methods=["POST"])
def handle_account_deletion_notification():
    data = request.get_json()
    app.logger.info("Received POST deletion notification: %s", data)
    return jsonify({"status": "success", "message": "Notification received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
