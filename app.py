import hashlib
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Enable debug-level logging
logging.basicConfig(level=logging.INFO)

# Your eBay verification token
EXPECTED_TOKEN = "mCk87t3oXZQfEpYs2RuJpGbvTnqW9cUL1DJHMe5sKFiAWla0xBYzNh4g"
# Your callback URL (same as the one in eBay Developer Portal)
EXPECTED_ENDPOINT = "https://pokemon-card-app.onrender.com/marketplace-deletion-verification"

@app.route("/marketplace-deletion-verification", methods=["GET"])
def verify_token():
    # Log everything from eBay for debugging
    app.logger.info(f"Received GET request with args: {request.args}")

    challenge_code = request.args.get("challenge_code")
    token_from_ebay = request.args.get("token")

    if token_from_ebay != EXPECTED_TOKEN:
        return jsonify({
            "status": "error",
            "message": f"Invalid token received: {token_from_ebay or 'None'}",
            "received_args": request.args
        }), 400

    if challenge_code:
        # Concatenate challengeCode, verificationToken, and endpoint
        data_to_hash = challenge_code + EXPECTED_TOKEN + EXPECTED_ENDPOINT
        hashed_value = hashlib.sha256(data_to_hash.encode('utf-8')).hexdigest()
        return jsonify({"challengeResponse": hashed_value})

    return jsonify({
        "status": "error",
        "message": "No challenge_code received",
        "received_args": request.args
    }), 400

@app.route("/marketplace-account-deletion-notification", methods=["POST"])
def handle_deletion_notification():
    notification_data = request.get_json()
    app.logger.info(f"Received deletion notification: {notification_data}")
    return jsonify({"status": "success", "message": "Notification received successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
