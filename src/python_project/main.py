"""Main entry point for the note-taking application."""

import typer
from typing_extensions import Annotated
from . import logic

app = typer.Typer()

@app.command()
def add(content: str):
    """Add a new note."""
    note = logic.add_note(content)
    print(f"Added note: \"{note['content']}\"")

@app.command()
def list():
    """List all notes."""
    notes = logic.list_notes()
    if not notes:
        print("No notes yet.")
        return
    for note in notes:
        print(f"{note['id']}: {note['content']}")

@app.command()
def clear(
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            prompt="Are you sure you want to clear all notes?",
            help="Force deletion without confirmation.",
        ),
    ] = False,
):
    """Clear all notes."""
    if force:
        logic.clear_notes()
        print("All notes cleared.")
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    app() 