import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timezone


OUTPUT_DIR = "nyt_opensudoku"


def prettify_xml(elem):
    rough = ET.tostring(elem, encoding="utf-8")
    reparsed = minidom.parseString(rough)
    return reparsed.toprettyxml(indent="  ", encoding="utf-8")


def date_to_epoch_ms(date_str: str) -> int:
    """
    Convert YYYY-MM-DD → epoch milliseconds
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)


def puzzle_to_cells_data(puzzle: str) -> str:
    """
    Convert 81-char puzzle string into OpenSudoku cells_data format.
    """
    parts = ["version: 4&#10;"]

    for ch in puzzle:
        if ch == "0":
            parts.append("0|0|0|1|")
        else:
            parts.append(f"{ch}|0|0|0|")

    return "".join(parts)


def ensure_collection_file(difficulty, created_ts):
    """
    Create or load a difficulty collection file.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    filepath = os.path.join(
        OUTPUT_DIR,
        f"nyt_{difficulty}.opensudoku"
    )

    if os.path.exists(filepath):
        tree = ET.parse(filepath)
        root = tree.getroot()
        folder = root.find("folder")
        return tree, root, folder, filepath

    # Create new structure
    root = ET.Element("opensudoku")
    root.set("version", "3")

    folder = ET.SubElement(root, "folder")
    folder.set("name", f"NYT Sudoku - {difficulty.capitalize()}")
    folder.set("created", str(created_ts))

    tree = ET.ElementTree(root)
    return tree, root, folder, filepath


def append_puzzle(entry):
    difficulty = entry["difficulty"]
    puzzle = entry["puzzle"]
    date = entry["date"]

    created_ts = date_to_epoch_ms(date)

    tree, root, folder, filepath = ensure_collection_file(
        difficulty,
        created_ts
    )

    cells_data = puzzle_to_cells_data(puzzle)

    # Duplicate check
    for g in folder.findall("game"):
        if g.get("cells_data") == cells_data:
            print(f"Skipping duplicate {difficulty} {date}")
            return

    game = ET.SubElement(folder, "game")

    game.set("created", str(created_ts))
    game.set("state", "1")
    game.set("mistake_counter", "0")
    game.set("hint_usage", "0")
    game.set("time", "0")
    game.set("last_played", "0")
    game.set("cells_data", cells_data)

    # Credits string
    game.set(
        "user_note",
        f"NYT Sudoku | {date} | {difficulty}"
    )

    # Minimal command stack (required but can be empty)
    game.set("command_stack", "0|")

    xml_bytes = prettify_xml(root)

    xml_bytes = xml_bytes.decode("utf-8").replace("&amp;#10;", "&#10;")

    with open(filepath, "w") as f:
        f.write(xml_bytes)

    print(f"Appended {difficulty} puzzle ({date})")


def append_all(puzzles):
    for entry in puzzles:
        append_puzzle(entry)