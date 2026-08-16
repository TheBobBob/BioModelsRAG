import json
from datetime import datetime
from pathlib import Path


def get_chat_directory(output_path):
    """Return the directory where chat sessions are stored."""

    chat_dir = Path(output_path) / "chats"
    chat_dir.mkdir(parents=True, exist_ok=True)

    return chat_dir


def create_session_id():
    """Create a unique session ID."""

    return datetime.now().strftime("%Y%m%d_%H%M%S")


def load_chat_history(output_path, session=None):
    """
    Load an existing chat session.

    If session is None, start a new conversation.
    """

    if session is None:
        return []

    chat_dir = get_chat_directory(output_path)
    chat_file = chat_dir / f"{session}.json"

    if not chat_file.exists():
        raise FileNotFoundError(
            f"Chat session not found: {session}"
        )

    with open(chat_file, "r") as f:
        data = json.load(f)

    return data["messages"]


def save_chat_history(
    output_path,
    history,
    session=None,
):
    """Save a chat session."""

    chat_dir = get_chat_directory(output_path)

    if session is None:
        session = create_session_id()

    chat_file = chat_dir / f"{session}.json"

    data = {
        "session_id": session,
        "created_at": datetime.now().isoformat(),
        "messages": history,
    }

    with open(chat_file, "w") as f:
        json.dump(
            data,
            f,
            indent=4,
        )

    print(f"\nChat saved to: {chat_file}")

    return session