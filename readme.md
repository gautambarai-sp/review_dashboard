# 🍽️ AI Review Intelligence Dashboard (MVP)

An end-to-end **AI-powered review analysis dashboard** built from scratch to help restaurants understand customer feedback through **insight, confidence, and intelligence**, not just raw ratings.

This project focuses on:
- Turning reviews into actionable insights
- Identifying trustworthy feedback using confidence scoring
- Highlighting complaints to drive improvement
- Demonstrating real-world AI system design (not just models)

> ⚠️ This is a **learning + capability-building project**, not a commercial product.

---

## 🎯 Problem Statement

Restaurants receive large volumes of customer reviews, but:
- Reviews are emotional and unstructured
- Important complaints get buried
- Not all feedback is equally trustworthy
- Responding and learning takes time

**Goal:**  
Build a dashboard that converts raw reviews into **clear intelligence** that helps restaurants learn from mistakes and track performance over time.

---

## 🧠 Key Concepts Implemented

- **Hybrid Sentiment Analysis**
  - Combines rating-based sentiment and text-based sentiment
  - Resolves mismatches intelligently (text > rating)

- **Confidence Scoring (0–100)**
  - Estimates how trustworthy and useful a review is
  - Based on verification, text richness, and sentiment alignment
  - Avoids absolute “true/false” labeling

- **Insight-First Dashboard**
  - Performance trends over time
  - High-confidence complaints highlighted
  - Focus on learning, not vanity metrics

---

## 🏗️ Project Architecture

ai-review-dashboard/
│
├── data/
│   └── sample_reviews.csv
│
├── backend/
│   ├── preprocessing.py
│   └── schema.py
│
├── dashboard/
│   └── app.py
│
├── requirements.txt
└── README.md   (optional for now)

---

## 📊 Dashboard Features (Current MVP)

### 1. Restaurant Performance Overview
- Total number of reviews
- Average rating
- % of high-confidence reviews
- Rating trend over time

### 2. Hybrid Sentiment Analysis
- Rating-based sentiment (1–5 stars)
- Text-based sentiment (rule-based MVP)
- Hybrid resolver to handle mismatches

### 3. Confidence-Based Complaints
- Highlights **negative reviews with high confidence**
- Helps restaurants focus on real problems

### 4. Transparency
- Confidence score shown per review
- Raw and processed data visible

---

## 🧪 How Confidence Scoring Works (Simplified)

Each review starts with a base score of **50**.

Signals applied:
- +20 → Verified visit
- +10 → Detailed review (>20 words)
- -20 → Very short review (<5 words)
- +10 → Rating & text sentiment match
- -10 → Rating & text sentiment mismatch

Final score is capped between **0–100**.

Confidence levels:
- 🟢 80–100 → High confidence
- 🟡 40–79 → Medium confidence
- 🔴 0–39 → Low confidence

> This estimates **trustworthiness**, not factual correctness.

---

## 🚀 Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
