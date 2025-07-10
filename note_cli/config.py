from pydantic import BaseModel, Field
import os
import configparser

# --- Configuration Setup ---
APP_NAME = "note-cli"
APP_DIR = os.path.expanduser(f"~/.{APP_NAME}")
CONFIG_FILE = os.path.join(APP_DIR, "config.ini")
os.makedirs(APP_DIR, exist_ok=True)

class Theme(BaseModel):
    """Color theme for the application."""
    id_style: str = "cyan"
    title_style: str = "magenta"
    tag_style: str = "green"
    date_style: str = "blue"
    panel_border_style: str = "yellow"
    error_style: str = "bold red"
    success_style: str = "bold green"
    info_style: str = "bold cyan"

class Settings(BaseModel):
    """Application settings."""
    database_path: str = os.path.join(APP_DIR, "notes.db")
    default_editor: str = Field(os.environ.get("EDITOR", "default"), description="Your default text editor.")
    theme: Theme = Theme()

def save_config(settings: Settings):
    """Saves the current settings to the config file."""
    parser = configparser.ConfigParser()
    parser["main"] = {
        "database_path": settings.database_path,
        "default_editor": settings.default_editor
    }
    parser["theme"] = settings.theme.dict()
    with open(CONFIG_FILE, "w") as f:
        parser.write(f)

def load_config() -> Settings:
    """Loads settings from the config file, creating it if it doesn't exist."""
    if not os.path.exists(CONFIG_FILE):
        default_settings = Settings()
        save_config(default_settings)
        return default_settings

    parser = configparser.ConfigParser()
    parser.read(CONFIG_FILE)

    theme_settings = {k: v for k, v in parser.items("theme")} if parser.has_section("theme") else {}
    main_settings = {k: v for k, v in parser.items("main")} if parser.has_section("main") else {}

    return Settings(
        database_path=main_settings.get("database_path", os.path.join(APP_DIR, "notes.db")),
        default_editor=main_settings.get("default_editor", os.environ.get("EDITOR", "default")),
        theme=Theme(**theme_settings)
    )

# Load settings on module import
settings = load_config() 