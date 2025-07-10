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
    assert result.exit_code == 0
    assert "Added note: \"Test note\"" in result.stdout
    notes = database.read_notes()
    assert len(notes) == 1
    assert notes[0]["content"] == "Test note"

def test_list_notes():
    """Test listing notes."""
    runner.invoke(app, ["add", "Note 1"])
    runner.invoke(app, ["add", "Note 2"])
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "1: Note 1" in result.stdout
    assert "2: Note 2" in result.stdout

def test_list_notes_empty():
    """Test listing notes when none exist."""
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "No notes yet." in result.stdout

def test_clear_notes():
    """Test clearing all notes with force."""
    runner.invoke(app, ["add", "A note to be cleared"])
    result = runner.invoke(app, ["clear", "--force"])
    assert result.exit_code == 0
    assert "All notes cleared." in result.stdout
    notes = database.read_notes()
    assert len(notes) == 0

def test_clear_notes_prompt_yes():
    """Test clearing all notes with prompt confirmation."""
    runner.invoke(app, ["add", "A note"])
    result = runner.invoke(app, ["clear"], input="y\n")
    assert result.exit_code == 0
    assert "All notes cleared." in result.stdout
    notes = database.read_notes()
    assert len(notes) == 0

def test_clear_notes_prompt_no():
    """Test cancelling clearing notes with prompt."""
    runner.invoke(app, ["add", "A note"])
    result = runner.invoke(app, ["clear"], input="n\n")
    assert result.exit_code == 0
    assert "Operation cancelled." in result.stdout
    notes = database.read_notes()
    assert len(notes) == 1 