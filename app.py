import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

# Your eBay verification token
EXPECTED_TOKEN = "mCk87t3oXZQfEpYs2RuJpGbvTnqW9cUL1DJHMe5sKFiAWla0xBYzNh4g"
# Your callback URL (same as the one in eBay Developer Portal)
EXPECTED_ENDPOINT = "https://pokemon-card-app.onrender.com/marketplace-deletion-verification"

@app.route("/marketplace-deletion-verification", methods=["GET"])
def verify_token():
    # Retrieve challenge_code and token from the query parameters
    challenge_code = request.args.get("challenge_code")
    token_from_ebay = request.args.get("token")

    # Check if the token from eBay matches the expected token
    if token_from_ebay != EXPECTED_TOKEN:
        return jsonify({"status": "error", "message": "Invalid token"}), 400

    if challenge_code:
        # Concatenate challengeCode, verificationToken, and endpoint
        data_to_hash = challenge_code + EXPECTED_TOKEN + EXPECTED_ENDPOINT

        # Create the SHA-256 hash
        hashed_value = hashlib.sha256(data_to_hash.encode('utf-8')).hexdigest()

        # Return the response with the challengeResponse field
        return jsonify({"challengeResponse": hashed_value})

    return jsonify({"status": "error", "message": "No challenge_code received"}), 400

@app.route("/marketplace-account-deletion-notification", methods=["POST"])
def handle_deletion_notification():
    # Example of receiving the POST notification (you can extend this to process the data)
    notification_data = request.get_json()

    # Example: just acknowledge that you received the notification
    print("Received deletion notification:", notification_data)

    # Respond with an HTTP status code indicating success (200 OK)
    return jsonify({"status": "success", "message": "Notification received successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Port 10000 or any port of your choice
