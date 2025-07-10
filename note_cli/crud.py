
import random
import secrets  # Added for cryptographically secure random
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from typing import Generator, List, Optional, Any
from . import database, encryption

def get_db() -> Generator[Session, None, None]:
    """Yield a database session."""
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _commit_changes(db: Session, obj: Any) -> None:
    """Helper function to commit changes and refresh an object."""
    db.commit()
    db.refresh(obj)

# --- Note CRUD ---
def add_note(db: Session, title: str, content: str, tags: list[str], encryptor: encryption.Encryptor) -> database.Note:
    """Add a new note to the database."""
    encrypted_content = encryptor.encrypt(content)
    db_note = database.Note(title=title, encrypted_content=encrypted_content, tags=",".join(tags))
    db.add(db_note)
    _commit_changes(db, db_note)
    return db_note

def get_all_notes(db: Session, tag_filter: str = None, include_archived=False) -> List[database.Note]:
    """Retrieve all notes based on filters."""
    query = db.query(database.Note).filter(database.Note.is_deleted == False)
    if not include_archived:
        query = query.filter(database.Note.is_archived == False)
    if tag_filter:
        query = query.filter(database.Note.tags.ilike(f"%{tag_filter}%"))
    return query.order_by(desc(database.Note.is_pinned), desc(database.Note.created_at)).all()

def get_note_by_id(db: Session, note_id: int) -> Optional[database.Note]:
    """Get a note by its ID."""
    return db.query(database.Note).filter(database.Note.id == note_id, database.Note.is_deleted == False).first()

def update_note(db: Session, note_id: int, title: str, content: str, tags: list[str], encryptor: encryption.Encryptor) -> Optional[database.Note]:
    """Update an existing note."""
    db_note = get_note_by_id(db, note_id)
    if db_note:
        # Create a revision before updating
        revision = database.NoteRevision(note_id=db_note.id, encrypted_content=db_note.encrypted_content)
        db.add(revision)

        db_note.title = title
        db_note.encrypted_content = encryptor.encrypt(content)
        db_note.tags = ",".join(tags)
        _commit_changes(db, db_note)
    return db_note

def soft_delete_note(db: Session, note_id: int) -> Optional[database.Note]:
    """Soft delete a note by setting is_deleted to True."""
    db_note = get_note_by_id(db, note_id)
    if db_note:
        db_note.is_deleted = True
        db_note.is_pinned = False
        db_note.is_archived = False
        _commit_changes(db, db_note)
    return db_note

def search_notes(db: Session, query: str, encryptor: encryption.Encryptor) -> List[database.Note]:
    """Search notes based on a query string."""
    notes = get_all_notes(db, include_archived=True)
    search_filter = query.lower()
    results = []
    for note in notes:
        try:
            content = encryptor.decrypt(note.encrypted_content)
            if (search_filter in note.title.lower() or 
                search_filter in content.lower() or 
                search_filter in note.tags.lower()):
                results.append(note)
        except ValueError:
            # Decryption failed (e.g., wrong password), skip note
            continue
    return results

def toggle_pin_note(db: Session, note_id: int) -> Optional[database.Note]:
    """Toggle the pinned status of a note."""
    db_note = get_note_by_id(db, note_id)
    if db_note:
        db_note.is_pinned = not db_note.is_pinned
        _commit_changes(db, db_note)
    return db_note

def toggle_archive_note(db: Session, note_id: int) -> Optional[database.Note]:
    """Toggle the archived status of a note."""
    db_note = get_note_by_id(db, note_id)
    if db_note:
        db_note.is_archived = not db_note.is_archived
        _commit_changes(db, db_note)
    return db_note

def get_trashed_notes(db: Session) -> List[database.Note]:
    """Get all trashed notes."""
    return db.query(database.Note).filter(database.Note.is_deleted == True).all()

def restore_note(db: Session, note_id: int) -> Optional[database.Note]:
    """Restore a deleted note."""
    db_note = db.query(database.Note).filter(database.Note.id == note_id, database.Note.is_deleted == True).first()
    if db_note:
        db_note.is_deleted = False
        _commit_changes(db, db_note)
    return db_note

def empty_trash(db: Session) -> int:
    """Permanently delete all trashed notes."""
    deleted_notes = db.query(database.Note).filter(database.Note.is_deleted == True)
    count = deleted_notes.count()
    deleted_notes.delete(synchronize_session=False)
    db.commit()
    return count

def get_random_note(db: Session) -> Optional[database.Note]:
    """Get a random note using a cryptographically secure method."""
    query = db.query(database.Note).filter(database.Note.is_deleted == False, database.Note.is_archived == False)
    count = query.count()
    if count > 0:
        offset = secrets.randbelow(count)  # Replaced with cryptographically secure alternative
        return query.offset(offset).first()
    return None

def get_stats(db: Session) -> dict:
    """Get statistics about notes."""
    total_notes = db.query(database.Note).filter(database.Note.is_deleted == False, database.Note.is_archived == False).count()
    total_archived = db.query(database.Note).filter(database.Note.is_deleted == False, database.Note.is_archived == True).count()
    total_trashed = db.query(database.Note).filter(database.Note.is_deleted == True).count()
    all_tags = (note.tags for note in get_all_notes(db, include_archived=True) if note.tags)  # Replaced with generator expression
    tags_list = {tag.strip() for tags in all_tags for tag in tags.split(',') if tag.strip()}
    return {"total_notes": total_notes, "total_archived": total_archived, "total_trashed": total_trashed, "total_tags": len(tags_list)}

# --- Revision CRUD ---
def get_revisions_for_note(db: Session, note_id: int) -> List[database.NoteRevision]:
    """Get revisions for a specific note."""
    return db.query(database.NoteRevision).filter_by(note_id=note_id).order_by(desc(database.NoteRevision.created_at)).all()

def restore_revision(db: Session, revision_id: int) -> Optional[database.Note]:
    """Restore a note to a previous revision."""
    revision = db.query(database.NoteRevision).get(revision_id)
    if revision and revision.note:
        note = revision.note
        # Save current version as a new revision before overwriting
        current_revision = database.NoteRevision(note_id=note.id, encrypted_content=note.encrypted_content)
        db.add(current_revision)
        
        note.encrypted_content = revision.encrypted_content
        _commit_changes(db, note)
        return note
    return None

# --- Template CRUD ---
def add_template(db: Session, name: str, content: str) -> database.Template:
    """Add a new template."""
    template = database.Template(name=name, content=content)
    db.add(template)
    _commit_changes(db, template)
    return template

def get_template(db: Session, name: str) -> Optional[database.Template]:
    """Get a template by name."""
    return db.query(database.Template).filter_by(name=name).first()

def list_templates(db: Session) -> List[database.Template]:
    """List all templates."""
    return db.query(database.Template).all()

def delete_template(db: Session, name: str) -> Optional[database.Template]:
    """Delete a template by name."""
    template = get_template(db, name)
    if template:
        db.delete(template)
        db.commit()
    return template 
