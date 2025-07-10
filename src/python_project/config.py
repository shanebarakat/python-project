"""Configuration for the note-taking application."""

from pathlib import Path

APP_NAME = "python-project"
APP_DIR = Path.home() / f".{APP_NAME}"
NOTES_FILE = APP_DIR / "notes.json" 

APP_DIR.mkdir(exist_ok=True) 