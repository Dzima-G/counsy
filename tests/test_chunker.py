from app.domains.documents.chunker import split_text


def test_split_text_returns_multiple_chunks() -> None:
    """Checks text splitting -> returns multiple fragments."""
    text = "Предложение номер один." * 200
    chunks = split_text(text)

    assert len(chunks) > 1, f"Expected > 1, got {len(chunks)}"
    assert all(isinstance(chunk, str) for chunk in chunks), "Expected True, got False"


def test_split_text_short_stays_single() -> None:
    """Checks a short text fragment -> remains a single whole."""
    chunks = split_text("Предложение номер один.")

    assert len(chunks) == 1, f"Expected 1, got {len(chunks)}"
