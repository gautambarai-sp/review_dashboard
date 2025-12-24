import streamlit as st
import pandas as pd

from backend.preprocessing import clean_text
from backend.schema import (
    rating_to_sentiment,
    text_to_sentiment,
    hybrid_sentiment,
    confidence_score
)

st.set_page_config(
    page_title="AI Review Dashboard",
    layout="wide"
)

st.title("🍽️ Restaurant Review Intelligence Dashboard")
st.markdown("Upload your restaurant reviews to generate insights.")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ----------------------------
    # Preprocessing
    # ----------------------------
    df["clean_text"] = df["review_text"].apply(clean_text)

    df["rating_sentiment"] = df["rating"].apply(rating_to_sentiment)
    df["text_sentiment"] = df["clean_text"].apply(text_to_sentiment)

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

    # ----------------------------
    # Overview Section
    # ----------------------------
    st.subheader("📊 Restaurant Performance Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Reviews", len(df))

    with col2:
        st.metric("Average Rating", round(df["rating"].mean(), 2))

    with col3:
        high_conf = (df["confidence_score"] >= 80).mean() * 100
        st.metric("High Confidence Reviews (%)", round(high_conf, 1))

    # ----------------------------
    # Rating Trend
    # ----------------------------
    st.subheader("📈 Rating Trend Over Time")
    df["review_date"] = pd.to_datetime(df["review_date"])
    trend = df.groupby("review_date")["rating"].mean()
    st.line_chart(trend)

    # ----------------------------
    # Complaints Section
    # ----------------------------
    st.subheader("⚠️ High-Confidence Complaints")

    complaints = df[
        (df["sentiment"] == "negative") &
        (df["confidence_score"] >= 60)
    ][["review_text", "confidence_score"]]

    if len(complaints) == 0:
        st.write("No high-confidence complaints found.")
    else:
        for _, row in complaints.iterrows():
            st.write(
                f"• {row['review_text']} "
                f"(Confidence: {row['confidence_score']})"
            )

    # ----------------------------
    # Raw Data Viewer
    # ----------------------------
    with st.expander("🔍 View Processed Review Data"):
        st.dataframe(df)
