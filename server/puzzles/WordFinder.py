# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 18:41:30 2026

@author: goatm
"""

import json
from pathlib import Path

# Folder where this script lives
BASE_DIR = Path(__file__).resolve().parent
WORDS_FILE = BASE_DIR / "words.txt"


def is_valid_solution_grid(grid):
    """Check grid is a 2D list and every cell is '#' or a single letter."""
    if not isinstance(grid, list) or not grid:
        return False

    for row in grid:
        if not isinstance(row, list):
            return False
        for cell in row:
            if not isinstance(cell, str):
                return False
            if cell == "#":
                continue
            if len(cell) != 1 or not cell.isalpha():
                return False
    return True


def extract_words_from_rows(grid):
    """Extract words from rows split by '#'."""
    words = []
    for row in grid:
        current = []
        for cell in row:
            if cell == "#":
                if len(current) >= 2:
                    words.append("".join(current))
                current = []
            else:
                current.append(cell)
        if len(current) >= 2:
            words.append("".join(current))
    return words


def extract_words_from_cols(grid):
    """Extract words from columns split by '#'."""
    words = []
    num_cols = max(len(row) for row in grid)

    for col in range(num_cols):
        current = []
        for row in grid:
            if col >= len(row):
                cell = "#"
            else:
                cell = row[col]

            if cell == "#":
                if len(current) >= 2:
                    words.append("".join(current))
                current = []
            else:
                current.append(cell)
        if len(current) >= 2:
            words.append("".join(current))
    return words


def load_existing_words(path):
    """Load existing words from words.txt (if present)."""
    if not path.exists():
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}


def main():
    json_files = list(BASE_DIR.glob("*.json"))
    if not json_files:
        print("No JSON files found.")
        return

    found_words = set()

    for json_path in json_files:
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        grid = data.get("solution")
        if not is_valid_solution_grid(grid):
            continue

        # Extract words
        words = []
        words.extend(extract_words_from_rows(grid))
        words.extend(extract_words_from_cols(grid))

        # Normalize to lowercase
        found_words.update(w.lower() for w in words)

    if not found_words:
        print("No words found.")
        return

    # Avoid duplicates already in file
    existing_words = load_existing_words(WORDS_FILE)
    new_words = sorted(found_words - existing_words)

    if not new_words:
        print("No new words to add.")
        return

    # Append to words.txt
    with open(WORDS_FILE, "a", encoding="utf-8") as f:
        for word in new_words:
            f.write(word + "\n")

    print(f"Added {len(new_words)} words to {WORDS_FILE.name}")


if __name__ == "__main__":
    main()
