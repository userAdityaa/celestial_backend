from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()
app = Flask(__name__)

RAPIDAPI_HOST = os.environ.get("RAPIDAPI_HOST")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")

@app.route("/user/tweets", methods=["GET"])
def get_user_tweets():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username is required."}), 400
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    
    # First API call to get the initial tweets
    url_initial = f"https://twitter154.p.rapidapi.com/user/tweets"
    params_initial = {
        "username": username,
        "limit": "20",
        "include_replies": "false",
        "include_pinned": "true"
    }
    
    try:
        response_initial = requests.get(url_initial, headers=headers, params=params_initial)
        response_initial.raise_for_status()
        data = response_initial.json()
        
        tweets = data.get("results", [])
        continuation_token = data.get("continuation_token")
        
        # Check if we need to fetch more tweets
        if len(tweets) < 40 and continuation_token:
            url_continuation = f"https://twitter154.p.rapidapi.com/user/tweets/continuation"
            params_continuation = {
                "username": username,
                "limit": "40",  # Request more to ensure total is between 40 and 50
                "continuation_token": continuation_token,
                "include_replies": "false"
            }
            response_continuation = requests.get(url_continuation, headers=headers, params=params_continuation)
            response_continuation.raise_for_status()
            continuation_data = response_continuation.json()
            
            # Combine results
            tweets += continuation_data.get("results", [])
            tweets = tweets[:50]  # Ensure no more than 50 tweets
        
        return jsonify({"tweets": tweets, "count": len(tweets)})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
