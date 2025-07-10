
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich.prompt import Prompt

from . import database
from .config import settings

console = Console(theme=settings.theme.dict())

def display_note_table(notes: list[database.Note], title="Your Notes"):
    """Display a list of notes in a table."""
    if not notes:
        console.print(f"[yellow]No notes found in {title.lower()}.[/yellow]")
        return

    table = Table(title=title, style=settings.theme.panel_border_style)
    table.add_column("ID", style=settings.theme.id_style, no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Title", style=settings.theme.title_style)
    table.add_column("Tags", style=settings.theme.tag_style)
    table.add_column("Revisions", justify="center")
    table.add_column("Last Updated", style=settings.theme.date_style)

    for note in notes:
        icons = []
        if note.is_pinned:
            icons.append("📌")
        if note.is_archived:
            icons.append("🗄️")
        
        status_icon = ''.join(icons)
        
        table.add_row(
            str(note.id),
            status_icon,
            note.title,
            note.tags,
            str(len(note.revisions)),
            note.updated_at.strftime("%Y-%m-%d %H:%M")
        )
    console.print(table)

def display_note_details(note: database.Note, content: str):
    """Display the full details of a single note, including decrypted content."""
    if not note:
        console.print("[error_style]Note not found.[/error_style]")
        return

    meta_text = Text()
    meta_text.append(f"Created: {note.created_at.strftime('%Y-%m-%d %H:%M')} | ")
    meta_text.append(f"Updated: {note.updated_at.strftime('%Y-%m-%d %H:%M')}\n")
    meta_text.append(f"Pinned: {'Yes' if note.is_pinned else 'No'} | ")
    meta_text.append(f"Archived: {'Yes' if note.is_archived else 'No'} | ")
    meta_text.append(f"Revisions: {len(note.revisions)}")

    title_panel = Panel(f"[bold {settings.theme.title_style}]{note.title}[/]", title="Title", border_style=settings.theme.title_style)
    content_panel = Panel(Markdown(content), title="Content (Encrypted 🔒)", border_style="green")
    tags_panel = Panel(f"[{settings.theme.tag_style}]{note.tags}[/]", title="Tags", border_style=settings.theme.tag_style)
    meta_panel = Panel(meta_text, title="Metadata", border_style=settings.theme.date_style)

    console.print(title_panel)
    console.print(content_panel)
    console.print(tags_panel)
    console.print(meta_panel)

def display_stats(stats: dict):
    """Display application statistics."""
    panel = Panel(
        f"[bold {settings.theme.id_style}]Active Notes:[/bold {settings.theme.id_style}] {stats['total_notes']}\n"
        f"[bold {settings.theme.date_style}]Archived Notes:[/bold {settings.theme.date_style}] {stats['total_archived']}\n"
        f"[bold {settings.theme.error_style}]In Trash:[/bold {settings.theme.error_style}] {stats['total_trashed']}\n"
        f"[bold {settings.theme.tag_style}]Unique Tags:[/bold {settings.theme.tag_style}] {stats['total_tags']}",
        title="Application Stats",
        border_style=settings.theme.panel_border_style
    )
    console.print(panel)

def display_revisions(revisions: list[database.NoteRevision]):
    """Display a list of revisions for a note."""
    if not revisions:
        console.print("[yellow]No revisions found for this note.[/yellow]")
        return
    
    table = Table(title="Note Revisions", style=settings.theme.panel_border_style)
    table.add_column("Revision ID", style=settings.theme.id_style)
    table.add_column("Saved At", style=settings.theme.date_style)
    
    for rev in revisions:
        table.add_row(str(rev.id), rev.created_at.strftime("%Y-%m-%d %H:%M"))
        
    console.print(table)

def display_templates(templates: list[database.Template]):
    """Display a list of available templates."""
    if not templates:
        console.print("[yellow]No templates created yet.[/yellow]")
        return
        
    table = Table(title="Available Templates", style=settings.theme.panel_border_style)
    table.add_column("Name", style=settings.theme.title_style)
    table.add_column("Content Snippet", style=settings.theme.tag_style)
    
    for t in templates:
        snippet = t.content[:80].replace('\n', ' ') + "..." if len(t.content) > 80 else t.content
        table.add_row(t.name, snippet)
        
    console.print(table)

def get_password() -> str:
    """Securely prompt for a password."""
    return Prompt.ask("[bold yellow]Enter your master password[/bold yellow]", password=True) 
