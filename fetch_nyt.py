import requests
import re
import json


URL = "https://www.nytimes.com/puzzles/sudoku"


def fetch_game_data():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    html = requests.get(URL, headers=headers).text

    # Extract window.gameData object
    match = re.search(r"window\.gameData\s*=\s*({.+?});", html, re.S)

    if not match:
        raise RuntimeError("window.gameData not found")

    json_text = match.group(1)

    idx = json_text.find("</script>")

    json_text = json_text[:idx]

    # Parse JSON
    data = json.loads(json_text)

    return data


def puzzle_to_string(puzzle_array):
    """
    Converts puzzle array to 81-character string.
    """
    return "".join(str(x) for x in puzzle_array)


def extract_all_difficulties(data):
    results = []

    for difficulty in ["easy", "medium", "hard"]:
        puzzle = data[difficulty]["puzzle_data"]["puzzle"]
        date = data[difficulty]["print_date"]
        results.append({
            "difficulty": difficulty, 
            "date": date,
            "puzzle": puzzle_to_string(puzzle)
        })

    return results