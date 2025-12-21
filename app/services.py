def analyze_text(text: str) -> dict:
    """
    Core business logic for content analysis.
    """
    length = len(text)
    preview = text[:30] + "..." if length > 30 else text

    return {
        "length": length,
        "preview": preview
    }
