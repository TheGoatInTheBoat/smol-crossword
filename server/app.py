from flask import Flask, jsonify, send_from_directory
from datetime import datetime
import os

app = Flask(__name__, static_folder="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUZZLES_DIR = os.path.join(BASE_DIR, "puzzles")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/puzzle")
def puzzle():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    puzzle_path = os.path.join(PUZZLES_DIR, f"{today}.json")

    print("Looking for:", puzzle_path)  # shows in Render logs

    if not os.path.exists(puzzle_path):
        return jsonify({"error": "Puzzle not found"}), 404

    with open(puzzle_path, "r") as f:
        return jsonify(__import__("json").load(f))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
