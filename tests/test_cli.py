from unittest.mock import patch, MagicMock

from biomodelsrag/cli import BioModelCLI


def test_ask():
    cli = BioModelCLI()

    fake_db = MagicMock()

    with patch(
        "cli.load_vector_db",
        return_value=fake_db,
    ) as mock_load_db, patch(
        "cli.generate_response",
        return_value="ATP is converted to ADP.",
    ) as mock_generate:

        cli.ask(
            "What happens to ATP?",
            "/tmp/test_db",
        )

    mock_load_db.assert_called_once_with(
        "/tmp/test_db"
    )

    mock_generate.assert_called_once_with(
        db=fake_db,
        query="What happens to ATP?",
        history=[],
        backend="groq",
        model="llama-3.3-70b-versatile",
        top_n=5,
    )