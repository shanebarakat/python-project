"""Database handling for the note-taking application."""

import json
from typing import List, Dict, Any
from . import config

def read_notes() -> List[Dict[str, Any]]:
    """Read notes from the JSON file."""
    if not config.NOTES_FILE.exists():
        return []
    with open(config.NOTES_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_notes(notes: List[Dict[str, Any]]) -> None:
    """Write notes to the JSON file."""
    with open(config.NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4) 