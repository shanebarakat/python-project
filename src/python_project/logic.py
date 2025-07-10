"""Core logic for the note-taking application."""

from typing import List, Dict, Any
from . import database

def add_note(content: str) -> Dict[str, Any]:
    """Add a new note."""
    notes = database.read_notes()
    new_note = {"id": len(notes) + 1, "content": content}
    notes.append(new_note)
    database.write_notes(notes)
    return new_note

def list_notes() -> List[Dict[str, Any]]:
    """List all notes."""
    return database.read_notes()

def clear_notes() -> None:
    """Clear all notes."""
    database.write_notes([]) 