# Pokémon Card Price Tracker

This app shows average raw and PSA 10 prices for popular Pokémon cards using dummy data.

## Setup (Windows)

1. **Install Python**
   - Get it from: https://www.python.org/downloads/windows/
   - During install, CHECK "Add Python to PATH"

2. **Open Command Prompt**
   - Press `Windows + R`, type `cmd`, press Enter

3. **Navigate to the folder**
   Example:
   > cd path\to\pokemon_card_price_tracker

4. **Create virtual environment**
   > python -m venv venv
   > venv\Scripts\activate

5. **Install dependencies**
   > pip install flask requests

6. **Run the app**
   > python app.py

7. **Visit in your browser**
   http://127.0.0.1:5000

Note: This version uses fake prices — we'll plug in the real eBay API next.