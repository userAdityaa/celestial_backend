from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

import os

RAPIDAPI_HOST = os.environ.get("RAPIDAPI_HOST")
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
RAPIDAPI_URL = os.environ.get("RAPIDAPI_URL")

if not RAPIDAPI_HOST or not RAPIDAPI_KEY:
    raise ValueError("RAPIDAPI_HOST or RAPIDAPI_KEY is not set")


@app.route("/get_timeline", methods=["GET"])
def get_timeline():
    screenname = request.args.get("screenname")
    if not screenname:
        return jsonify({"error": "Please provide a screenname."})


    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY,
    }
    params = {"screenname": screenname}

    try:
        response = requests.get(RAPIDAPI_URL, headers=headers, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)