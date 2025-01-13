from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)



@app.route("/get_timeline", methods=["GET"])
def get_timeline():
    screenname = request.args.get("screenname")
    if not screenname:
        return jsonify({"error": "Please provide a screenname."})


    headers = {
        "x-rapidapi-host": os.getenv(RAPIDAPI_HOST),
        "x-rapidapi-key": os.getenv(RAPIDAPI_KEY),
    }
    params = {"screenname": screenname}

    try:
        response = requests.get(os.getenv(RAPIDAPI_URL), headers=headers, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)