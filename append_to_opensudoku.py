import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

OUTPUT_DIR = "nyt_opensudoku"


def prettify_xml(elem):
    """Return pretty-printed XML string."""
    rough = ET.tostring(elem, encoding="utf-8")
    reparsed = minidom.parseString(rough)
    return reparsed.toprettyxml(indent="  ", encoding="utf-8")


def ensure_collection_file(difficulty):
    """
    Create a new .opensudoku file if it doesn't exist.
    Returns (tree, root, filepath)
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"nyt_{difficulty}.opensudoku")

    if os.path.exists(filepath):
        tree = ET.parse(filepath)
        root = tree.getroot()
        return tree, root, filepath

    # Create new collection
    root = ET.Element("opensudoku")

    ET.SubElement(root, "name").text = f"NYT Sudoku - {difficulty.capitalize()}"
    ET.SubElement(root, "author").text = "NYT auto-export"
    ET.SubElement(root, "source").text = "nytimes"
    ET.SubElement(root, "level").text = difficulty

    tree = ET.ElementTree(root)
    return tree, root, filepath


def append_puzzle(entry):
    difficulty = entry["difficulty"]
    puzzle = entry["puzzle"]
    date = entry["date"]

    tree, root, filepath = ensure_collection_file(difficulty)

    # Optional duplicate check
    for g in root.findall("game"):
        if g.get("data") == puzzle:
            print(f"Skipping duplicate ({difficulty}, {date})")
            return

    game = ET.SubElement(root, "game")
    game.set("data", puzzle)

    # Non-standard but useful metadata (ignored by most apps)
    game.set("date", date)

    # Write file
    xml_bytes = prettify_xml(root)
    with open(filepath, "wb") as f:
        f.write(xml_bytes)

    print(f"Appended {difficulty} puzzle ({date})")


def append_all(puzzles):
    for entry in puzzles:
        append_puzzle(entry)