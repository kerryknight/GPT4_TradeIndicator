from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Load the API key from /etc/secrets/IndicatorKey.txt
API_KEY_FILE_PATH = "/etc/secrets/IndicatorKey.txt"
try:
    with open(API_KEY_FILE_PATH, 'r') as file:
        OPENAI_API_KEY = file.read().strip()  # Read and strip any newline characters
except FileNotFoundError:
    raise ValueError(f"API key file not found at {API_KEY_FILE_PATH}")

API_URL = "https://api.openai.com/v1/completions"
TRADE_URL = "https://app.optionalpha.com/hook/H7IpT8jlMTe56eb3fdeeed3b8692f1809/fbcbdf14ba6977acfbabd4dddc8536592fe3d9"
NO_TRADE_URL = "https://app.optionalpha.com/hook/H7IpT8jlMT76e7caa8265bd535724bc9e/38f5df815e1bbac01b7390b70eac24aa774096"

def ask_gpt(prompt):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4",
        "prompt": prompt,
        "max_tokens": 150,
    }
    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()
    return result["choices"][0]["text"].strip()

def fetch_world_events():
    # First prompt to fetch world events
    prompt = "What major world events have occurred in the last 24 hours?"
    return ask_gpt(prompt)

def analyze_impact(events):
    # Second prompt to analyze impact on SPX
    prompt = (
        f"Based on historical data and your best judgment, "
        f"will any of these events affect the price of SPX by more than 1.5 basis points?\n\n{events}"
    )
    return ask_gpt(prompt)

def is_trade_recommended(impact_analysis):
    # Check if GPT's response suggests stability by looking for "no" as the response
    return "no" in impact_analysis.lower()

def trigger_option_alpha(url):
    try:
        response = requests.post(url)
        return response.status_code == 200
    except Exception as e:
        print(f"Error triggering Option Alpha: {e}")
        return False

@app.route("/option_alpha_trigger", methods=["GET", "POST"])
def option_alpha_trigger():
    try:
        # Step 1: Get recent events
        events = fetch_world_events()
        
        # Step 2: Analyze if the events will affect SPX by more than 1.5 basis points
        impact_analysis = analyze_impact(events)
        
        # Step 3: Determine if we should trigger the trade or no-trade webhook
        if is_trade_recommended(impact_analysis):
            # If GPT suggests stability, trigger trade URL
            success = trigger_option_alpha(TRADE_URL)
            message = "Market conditions are stable; trading triggered." if success else "Failed to trigger trading."
        else:
            # If GPT suggests volatility, trigger no-trade URL
            success = trigger_option_alpha(NO_TRADE_URL)
            message = "High volatility detected; trading paused." if success else "Failed to trigger no-trade."

        # Output the result message
        return jsonify({"status": "success", "message": message}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
