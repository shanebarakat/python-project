# Note-CLI: A Comprehensive, Encrypted, Command-Line Note-Taking App

Note-CLI is a professional-grade, feature-packed note-taking application that runs entirely in your terminal. It's designed for developers, writers, and anyone who values security, efficiency, and extensive customizability in their workflow. All your notes are encrypted at rest, ensuring your data remains private.

## ✨ Core Features

-   **End-to-End Encryption**: Note content is encrypted with a key derived from your master password using strong cryptographic standards (`PBKDF2HMAC` and `AES`).
-   **Interactive Editing**: Edit notes in your default system editor (`$EDITOR`) for a seamless writing experience.
-   **Rich and Themed Interface**: A beautiful terminal UI powered by `rich`, with customizable color themes.
-   **Note Revisions**: Every edit creates a version history. View and restore previous versions of any note.
-   **Note Templates**: Create and manage templates to quickly bootstrap new notes with predefined content.
-   **Note Pinning & Archiving**: Pin important notes, and archive others to hide them from the main view without deleting them.
-   **Tagging and Filtering**: Organize your notes with tags and filter your note list by any tag.
-   **Powerful Search**: Instantly search across note titles, content, and tags (requires password for decryption).
-   **Safe Deletes with a Trash Can**: Deleted notes go to a trash can, where you can list, restore, or permanently empty them.
-   **Configuration File**: Customize the app via a simple `.ini` file located at `~/.note-cli/config.ini`.
-   **Persistent Storage**: Notes are saved in a local SQLite database.

## 🚀 Installation

1.  **Clone the repository:** `git clone <repository-url> && cd note-cli-project`
2.  **Install the application:** `pip install -e .`

The first time you run a command, the application will automatically create a configuration file and a database in `~/.note-cli/`.

## 🔐 A Note on Security

On the first command that requires encryption or decryption (like `add`, `show`, `edit`, `search`), you will be prompted for a master password. This password is used to generate the encryption key for the current session. It is **never stored**.

**If you forget your password, your notes cannot be recovered.**

## Usage

### Core Note Commands
-   **`note`**: List all active (non-archived) notes.
-   **`note add --title "..."`**: Add a new note. You'll be prompted for tags and content.
-   **`note add --template <name>`**: Create a new note from a template.
-   **`note show <ID>`**: Decrypt and display a single note.
-   **`note edit <ID>`**: Decrypt and open a note in your default editor. Saving will create a new revision.
-   **`note update <ID> --title "..." --tags "..."`**: Update a note's title and/or tags.
-   **`note delete <ID>`**: Move a note to the trash.
-   **`note search <query>`**: Search through encrypted notes.
-   **`note pin <ID>`**: Pin or unpin a note.
-   **`note archive <ID>`**: Archive or unarchive a note.
-   **`note list --archived`**: View a list of your archived notes.

### Revision Management
-   **`note revision list <NOTE_ID>`**: View the revision history for a note.
-   **`note revision restore <REVISION_ID>`**: Restore a note to a previous version. The current version will be saved as a new revision.

### Template Management
-   **`note template list`**: List all available templates.
-   **`note template add <name>`**: Create a new template by opening your text editor.
-   **`note template delete <name>`**: Delete a template.

### Trash Management
-   **`note trash list`**: View all notes in the trash.
-   **`note trash restore <ID>`**: Restore a note from the trash.
-   **`note trash empty`**: Permanently delete all notes in the trash.

### Utilities
-   **`note stats`**: Show application statistics.
-   **`note config set <section>.<key> <value>`**: (Coming soon) A way to edit the config from the CLI. For now, edit `~/.note-cli/config.ini` directly. 