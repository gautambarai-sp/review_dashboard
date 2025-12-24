import sys, os
sys.path.append(os.path.abspath(""))

import streamlit as st
import pandas as pd

from backend.preprocessing import clean_text
from backend.schema import *
from backend.aspects import *
from backend.responses import generate_response
from backend.learning import log_response_feedback
from backend.prioritization import compute_priority_scores
from backend.ml_sentiment import ml_text_sentiment

st.set_page_config(page_title="Review Intelligence", layout="wide")

st.markdown("<h1>Review Intelligence</h1>", unsafe_allow_html=True)

uploaded = st.file_uploader("Upload Reviews CSV", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    df["review_date"] = pd.to_datetime(df["review_date"])
    df["clean_text"] = df["review_text"].apply(clean_text)

    df["rating_sentiment"] = df["rating"].apply(rating_to_sentiment)
    df["rule_text_sentiment"] = df["clean_text"].apply(text_to_sentiment)
    df["ml_text_sentiment"] = df["clean_text"].apply(ml_text_sentiment)
    df["text_sentiment"] = df.apply(
        lambda x: final_text_sentiment(
            x["clean_text"],
            x["rule_text_sentiment"],
            x["ml_text_sentiment"]
        ),
        axis=1
    )

    df["sentiment"] = df.apply(
        lambda x: hybrid_sentiment(
            x["rating_sentiment"],
            x["text_sentiment"]
        ),
        axis=1
    )

    df["confidence_score"] = df.apply(
        lambda x: confidence_score(
            x["clean_text"],
            x["verified_visit"],
            x["rating_sentiment"],
            x["text_sentiment"]
        ),
        axis=1
    )

    df["aspects"] = df["clean_text"].apply(detect_aspects)
    df = df.explode("aspects")
    df["issue"] = df.apply(
        lambda x: extract_issue(x["aspects"], x["clean_text"])
        if pd.notnull(x["aspects"]) else None,
        axis=1
    )

    complaints = df[
        (df["sentiment"] == "negative") &
        (df["confidence_score"] >= 60)
    ]

    priority = compute_priority_scores(complaints)

    st.subheader("🚑 Fix This First")
    st.error(priority.iloc[0]["issue"])

    st.subheader("💬 Response Assistant")
    row = complaints.iloc[0]
    response = generate_response(row["aspects"], "negative", row["issue"])
    edited = st.text_area("Response", response)

    if st.button("Accept"):
        log_response_feedback(row["review_id"], row["aspects"], row["issue"], edited, "accepted")
        st.success("Saved")
