
import typer
import json
from typing_extensions import Annotated
from typing import Optional
from . import crud, database, display, encryption, config

# --- App State ---
# This dictionary will hold our session-wide objects, like the encryptor
state = {"encryptor": None}

# --- Main App ---
app = typer.Typer(rich_markup_mode="markdown")
db_session = next(crud.get_db())

def get_note_or_exit(note_id: int):
    note = crud.get_note_by_id(db_session, note_id)
    if not note:
        display.console.print(f"[error_style]Note {note_id} not found.[/error_style]")
        raise typer.Exit(1)
    return note

def get_encryptor():
    """Lazily initialize and return a session-wide encryptor."""
    if state.get("encryptor") is None:
        password = display.get_password()
        try:
            state["encryptor"] = encryption.Encryptor(password)
        except Exception as e:
            display.console.print(f"[error_style]Failed to initialize encryptor: {e}[/error_style]")
            raise typer.Exit(1) 
    return state["encryptor"]

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    A comprehensive, encrypted, command-line note-taking app with versioning.
    Defaults to `list` if no command is specified.
    """
    database.init_db()
    if ctx.invoked_subcommand is None:
        list_notes()

# --- Core Note Commands ---
@app.command()
def add(
    title: Annotated[str, typer.Option(prompt=True)],
    content: Annotated[Optional[str], typer.Argument(help="Initial content. Leave empty to use editor.")] = None,
    tags: Annotated[str, typer.Option("--tags", "-t", prompt="Tags (comma-separated)", default="")] = "",
    template: Annotated[Optional[str], typer.Option("--template", help="Create note from a template.")] = None,
):
    """Add a new encrypted note."""
    if template:
        template_obj = crud.get_template(db_session, template)
        if not template_obj:
            display.console.print(f"[error_style]Template '{template}' not found.[/error_style]")
            raise typer.Exit(1)
        final_content = template_obj.content
    else:
        final_content = content or ""
    
    # Get content from editor if it's empty
    if not final_content:
        final_content = typer.edit(text="", extension=".md")
        if final_content is None:
            display.console.print(":stop_sign: [yellow]Note creation cancelled.[/yellow]")
            raise typer.Exit()
            
    tag_list = (tag.strip() for tag in tags.split(",") if tag.strip())
    note = crud.add_note(db_session, title, final_content, tag_list, get_encryptor())
    display.console.print(f":sparkles: [success_style]Note '[/success_style]{note.title}[success_style]' added successfully![/success_style]")

@app.command(name="list")
def list_notes(
    tag: Annotated[Optional[str], typer.Option("--tag", "-t", help="Filter notes by tag.")] = None,
    archived: Annotated[bool, typer.Option("--archived", "-a", help="Include archived notes.")] = False
):
    """List all notes. Pinned notes are shown first."""
    notes = crud.get_all_notes(db_session, tag_filter=tag, include_archived=archived)
    display.display_note_table(notes)

@app.command()
def show(note_id: int):
    """Show the full decrypted content of a single note."""
    note = get_note_or_exit(note_id)
    try:
        decrypted_content = get_encryptor().decrypt(note.encrypted_content)
        display.display_note_details(note, decrypted_content)
    except ValueError as e:
        display.console.print(f"[error_style]{e}[/error_style]")

@app.command()
def edit(note_id: int):
    """Edit a note's content using the default system editor."""
    note = get_note_or_exit(note_id)
    
    try:
        decrypted_content = get_encryptor().decrypt(note.encrypted_content)
        edited_content = typer.edit(decrypted_content, extension=".md")
        if edited_content is None:
            display.console.print(":stop_sign: [yellow]Edit cancelled.[/yellow]")
            raise typer.Exit()
        
        updated_note = crud.update_note(db_session, note_id, note.title, edited_content, note.tags.split(','), get_encryptor())
        display.console.print(f":pencil: [success_style]Note {note_id} updated successfully![/success_style]")
    except ValueError as e:
        display.console.print(f"[error_style]{e}[/error_style]")

@app.command()
def update(note_id: int, title: str, tags: str):
    """Update a note's title and/or tags."""
    # This is a simplified version. A more robust one would fetch note first.
    # To update content, use 'edit'
    note = get_note_or_exit(note_id)
    
    decrypted_content = get_encryptor().decrypt(note.encrypted_content) # Keep existing content
    updated_note = crud.update_note(db_session, note_id, title, decrypted_content, tags.split(','), get_encryptor())
    display.console.print(f":pencil: [success_style]Note {note_id} metadata updated successfully![/success_style]")


@app.command()
def delete(note_id: int):
    """Move a note to the trash."""
    note = crud.soft_delete_note(db_session, note_id)
    display.console.print(f":wastebasket: [yellow]Note {note_id} moved to trash.[/yellow]")

@app.command()
def search(query: str):
    """Search for notes by title, content, or tags (requires password)."""
    notes = crud.search_notes(db_session, query, get_encryptor())
    display.display_note_table(notes, title=f"Search Results for '{query}'")

@app.command()
def pin(note_id: int):
    """Pin or unpin a note."""
    note = crud.toggle_pin_note(db_session, note_id)
    status = "pinned" if note.is_pinned else "unpinned"
    display.console.print(f":pushpin: [info_style]Note {note_id} has been {status}.[/info_style]")

@app.command()
def archive(note_id: int):
    """Archive or unarchive a note."""
    note = crud.toggle_archive_note(db_session, note_id)
    status = "archived" if note.is_archived else "unarchived"
    display.console.print(f"🗄️ [info_style]Note {note_id} has been {status}.[/info_style]")

# --- Trash Sub-App ---
trash_app = typer.Typer(help="Manage trashed notes.")
app.add_typer(trash_app, name="trash")
# ... (trash commands are simple and don't need significant changes)
@trash_app.command(name="list")
def list_trash():
    """List all trashed notes."""
    notes = crud.get_trashed_notes(db_session)
    display.display_note_table(notes, title="Trash")
@trash_app.command()
def restore(note_id: int):
    """Restore a trashed note."""
    crud.restore_note(db_session, note_id)
@trash_app.command()
def empty():
    """Empty the trash."""
    crud.empty_trash(db_session)

# --- Revision Sub-App ---
revision_app = typer.Typer(help="Manage note revisions.")
app.add_typer(revision_app, name="revision")

@revision_app.command(name="list")
def list_revisions(note_id: int):
    """List all revisions for a given note."""
    revisions = crud.get_revisions_for_note(db_session, note_id)
    display.display_revisions(revisions)

@revision_app.command(name="restore")
def restore_revision(revision_id: int):
    """Restore a note to a previous revision."""
    note = crud.restore_revision(db_session, revision_id)
    display.console.print(f":rewind: [success_style]Note {note.id} restored to revision {revision_id}.[/success_style]")

# --- Template Sub-App ---
template_app = typer.Typer(help="Manage note templates.")
app.add_typer(template_app, name="template")

@template_app.command(name="add")
def add_template(name: str):
    """Create a new note template."""
    content = typer.edit(text="", extension=".md")
    crud.add_template(db_session, name, content)
    display.console.print(f":scroll: [success_style]Template '{name}' created.[/success_style]")

@template_app.command(name="list")
def list_templates():
    """List all available templates."""
    templates = crud.list_templates(db_session)
    display.display_templates(templates)

@template_app.command(name="delete")
def delete_template(name: str):
    """Delete a template."""
    crud.delete_template(db_session, name)
    display.console.print(f":wastebasket: [yellow]Template '{name}' deleted.[/yellow]")

# --- Utility Commands ---
@app.command()
def stats():
    """Show application statistics."""
    stats_data = crud.get_stats(db_session)
    display.display_stats(stats_data)

if __name__ == "__main__":
    app() 
