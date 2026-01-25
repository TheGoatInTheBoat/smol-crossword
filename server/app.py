from flask import Flask, jsonify, send_from_directory
from datetime import date
import json
import os

app = Flask(__name__, static_folder="static")

PUZZLE_DIR = os.path.join(os.path.dirname(__file__), "puzzles")

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/puzzle")
def puzzle():
    today = date.today().isoformat()
    path = os.path.join(PUZZLE_DIR, f"{today}.json")

    if not os.path.exists(path):
        return jsonify({"error": "Puzzle not available"}), 404

    try:
        with open(path, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    except Exception as e:
        print("PUZZLE LOAD ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
