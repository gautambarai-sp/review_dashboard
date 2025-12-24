try:
    from transformers import pipeline
    _sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )
    TRANSFORMERS_AVAILABLE = True
except Exception:
    TRANSFORMERS_AVAILABLE = False
    _sentiment_pipeline = None


def ml_text_sentiment(text: str) -> str:
    """
    Safe ML sentiment inference.
    Falls back to neutral if model is unavailable.
    """
    if not TRANSFORMERS_AVAILABLE:
        return "neutral"

    if not isinstance(text, str) or len(text.strip()) < 3:
        return "neutral"

    try:
        result = _sentiment_pipeline(text[:512])[0]["label"]
        return "positive" if result == "POSITIVE" else "negative"
    except Exception:
        return "neutral"
