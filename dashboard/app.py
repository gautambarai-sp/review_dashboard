import sys
import os

# --------------------------------------------------
# FIX: Add PROJECT ROOT to Python path (robust)
# --------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# --------------------------------------------------
# Standard imports
# --------------------------------------------------
import streamlit as st
import pandas as pd

# --------------------------------------------------
# Internal imports (NOW SAFE)
# --------------------------------------------------
from backend.preprocessing import clean_text
from backend.schema import (
    rating_to_sentiment,
    text_to_sentiment,
    final_text_sentiment,
    hybrid_sentiment,
    confidence_score
)
from backend.aspects import detect_aspects, extract_issue
from backend.responses import generate_response
from backend.learning import log_response_feedback
from backend.prioritization import compute_priority_scores
from backend.ml_sentiment import ml_text_sentiment

# --------------------------------------------------
# Streamlit Config
# --------------------------------------------------
st.set_page_config(
    page_title="Review Intelligence",
    page_icon="🍽️",
    layout="wide"
)

st.markdown(
    """
    <h1 style='margin-bottom:0;'>Review Intelligence</h1>
    <p style='color:gray; margin-top:0;'>
    Understand what customers feel. Fix what hurts most.
    </p>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# File Upload
# --------------------------------------------------
uploaded = st.file_uploader("Upload Reviews CSV", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    df["review_date"] = pd.to_datetime(df["review_date"])
    df["clean_text"] = df["review_text"].apply(clean_text)

    # ---------------- Sentiment ----------------
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

    # ---------------- Confidence ----------------
    df["confidence_score"] = df.apply(
        lambda x: confidence_score(
            x["clean_text"],
            x["verified_visit"],
            x["rating_sentiment"],
            x["text_sentiment"]
        ),
        axis=1
    )

    # ---------------- Aspect Intelligence ----------------
    df["aspects"] = df["clean_text"].apply(detect_aspects)
    df = df.explode("aspects")

    df["issue"] = df.apply(
        lambda x: extract_issue(x["aspects"], x["clean_text"])
        if pd.notnull(x["aspects"]) else None,
        axis=1
    )

    # ---------------- Complaints ----------------
    complaints = df[
        (df["sentiment"] == "negative") &
        (df["confidence_score"] >= 60) &
        (df["aspects"].notnull())
    ]

    # ---------------- Prioritization ----------------
    priority = compute_priority_scores(complaints)

    st.subheader("🚑 Fix This First")
    top_issue = priority.iloc[0]
    st.error(
        f"""
        **{top_issue['issue']}**  
        Aspect: {top_issue['aspects']}  
        Frequency: {top_issue['frequency']} complaints
        """
    )

    # ---------------- Response Assistant ----------------
    st.subheader("💬 Response Assistant")

    row = complaints.iloc[0]
    suggested = generate_response(
        row["aspects"], "negative", row["issue"]
    )

    edited = st.text_area(
        "Suggested Response (Editable)",
        suggested,
        height=150
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Accept"):
            log_response_feedback(
                row["review_id"],
                row["aspects"],
                row["issue"],
                edited,
                "accepted"
            )
            st.success("Response saved.")

    with col2:
        if st.button("❌ Reject"):
            log_response_feedback(
                row["review_id"],
                row["aspects"],
                row["issue"],
                edited,
                "rejected"
            )
            st.warning("Feedback recorded.")

