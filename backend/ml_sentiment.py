from transformers import pipeline

pipe = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def ml_text_sentiment(text: str):
    try:
        res = pipe(text[:512])[0]["label"]
        return "positive" if res == "POSITIVE" else "negative"
    except:
        return "neutral"
