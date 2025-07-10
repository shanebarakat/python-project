
"""Database handling for the note-taking application."""

import json
from typing import List, Dict, Any
from . import config

def read_notes() -> List[Dict[str, Any]]:
    """Read notes from the JSON file.
    
    Returns:
        List[Dict[str, Any]]: A list of notes, where each note is a dictionary.
            Returns an empty list if the file does not exist or contains invalid JSON.
    """
    if not config.NOTES_FILE.exists():
        return []
    with open(config.NOTES_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_notes(notes: List[Dict[str, Any]]) -> None:
    """Write notes to the JSON file.
    
    Args:
        notes (List[Dict[str, Any]]): The list of notes to write to the file.
    """
    with open(config.NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4) 
