from fetch_nyt import fetch_game_data, extract_all_difficulties
from append_to_opensudoku import append_all

if __name__ == "__main__":
    data = fetch_game_data()
    sudokus = extract_all_difficulties(data)

    append_all(sudokus)