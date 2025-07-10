
import pytest
from typer.testing import CliRunner
from python_project.main import app
from python_project import config, database

runner = CliRunner()

@pytest.fixture(autouse=True)
def temp_notes_file(tmp_path):
    """Fixture to use a temporary notes file for tests."""
    original_notes_file = config.NOTES_FILE
    config.NOTES_FILE = tmp_path / "test_notes.json"
    database.write_notes([])
    yield
    config.NOTES_FILE = original_notes_file

def test_add_note():
    """Test adding a note."""
    result = runner.invoke(app, ["add", "Test note"])
    if not (result.exit_code == 0):
        raise AssertionError
    if not ("Added note: \"Test note\"" in result.stdout):
        raise AssertionError
    notes = database.read_notes()
    if not (len(notes) == 1):
        raise AssertionError
    if not (notes[0]["content"] == "Test note"):
        raise AssertionError

def test_list_notes():
    """Test listing notes."""
    runner.invoke(app, ["add", "Note 1"])
    runner.invoke(app, ["add", "Note 2"])
    result = runner.invoke(app, ["list"])
    if not (result.exit_code == 0):
        raise AssertionError
    if not ("1: Note 1" in result.stdout):
        raise AssertionError
    if not ("2: Note 2" in result.stdout):
        raise AssertionError

def test_list_notes_empty():
    """Test listing notes when none exist."""
    result = runner.invoke(app, ["list"])
    if not (result.exit_code == 0):
        raise AssertionError
    if not ("No notes yet." in result.stdout):
        raise AssertionError

def test_clear_notes():
    """Test clearing all notes with force."""
    runner.invoke(app, ["add", "A note to be cleared"])
    result = runner.invoke(app, ["clear", "--force"])
    if not (result.exit_code == 0):
        raise AssertionError
    if not ("All notes cleared." in result.stdout):
        raise AssertionError
    notes = database.read_notes()
    if not (len(notes) == 0):
        raise AssertionError

def test_clear_notes_prompt_yes():
    """Test clearing all notes with prompt confirmation."""
    runner.invoke(app, ["add", "A note"])
    result = runner.invoke(app, ["clear"], input="y\n")
    if not (result.exit_code == 0):
        raise AssertionError
    if not ("All notes cleared." in result.stdout):
        raise AssertionError
    notes = database.read_notes()
    if not (len(notes) == 0):
        raise AssertionError

def test_clear_notes_prompt_no():
    """Test cancelling clearing notes with prompt."""
    runner.invoke(app, ["add", "A note"])
    result = runner.invoke(app, ["clear"], input="n\n")
    if not (result.exit_code == 0):
        raise AssertionError
    if not ("Operation cancelled." in result.stdout):
        raise AssertionError
    notes = database.read_notes()
    if not (len(notes) == 1):
        raise AssertionError


"""
This module contains tests for the note-taking application.
"""