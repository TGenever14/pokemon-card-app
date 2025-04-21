import hashlib
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Enable logging
logging.basicConfig(level=logging.INFO)

# Your eBay verification token and endpoint
EXPECTED_TOKEN = "mCk87t3oXZQfEpYs2RuJpGbvTnqW9cUL1DJHMe5sKFiAWla0xBYzNh4g"
EXPECTED_ENDPOINT = "https://pokemon-card-app.onrender.com/marketplace-deletion-verification"

@app.route("/")
def index():
    return "Service running!"

@app.route("/marketplace-deletion-verification", methods=["GET"])
def verify_token():
    challenge_code = request.args.get("challenge_code")
    token_from_ebay = request.args.get("token")  # May be None

    app.logger.info("Received GET request with args: %s", request.args)

    if not challenge_code:
        return jsonify({"status": "error", "message": "No challenge_code received"}), 400

    # Even if token is missing, proceed (eBay may not send it)
    data_to_hash = challenge_code + EXPECTED_TOKEN + EXPECTED_ENDPOINT
    hashed_value = hashlib.sha256(data_to_hash.encode('utf-8')).hexdigest()

    return jsonify({"challengeResponse": hashed_value})

@app.route("/marketplace-account-deletion-notification", methods=["POST"])
def handle_deletion_notification():
    notification_data = request.get_json()
    app.logger.info("Received deletion notification: %s", notification_data)
    return jsonify({"status": "success", "message": "Notification received successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
