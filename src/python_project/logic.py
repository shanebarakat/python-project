"""Core logic for the note-taking application."""

from typing import List, Dict, Any
from . import database

def add_note(content: str) -> Dict[str, Any]:
    """
    Add a new note.
    # Modified for join  Args:
        content (str): The content of the note to add.

    Returns:
        Dict[str, Any]: The newly created note dictionary.
    """
    notes = database.read_notes()
    new_note = {"id": len(notes) + 1, "content": content}
    notes.append(new_note)
    database.write_notes(notes)
    return new_note

def list_notes() -> List[Dict[str, Any]]:
    """
    List all notes.

    Returns:
        List[Dict[str, Any]]: A list of all notes.
    """
    return database.read_notes()

def clear_notes() -> None:
    """
    Clear all notes.

    This function removes all notes from the database.
    """
    database.write_notes([])