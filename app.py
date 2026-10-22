import os
from datetime import datetime

import pandas as pd
import streamlit as st

from labeler import BUSINESS, LABELS, label_comment, using_demo_mode

# ---- CHANGE THIS for your own business ---------------------------------
TITLE = "Pizza feedback"
RATING_MIN, RATING_MAX = 1, 5
LOW_RATING, HIGH_RATING = 2, 4      # a "low" rating is <= 2, a "high" rating is >= 4
CSV_FILE = "feedback.csv"
# -------------------------------------------------------------------------


def needs_review(label, rating):
    """Flag the rows we should read more carefully."""
    if label == "positive" and rating <= LOW_RATING:
        return True
    if label == "negative" and rating >= HIGH_RATING:
        return True
    if label not in ("positive", "negative"):   # "unclear" or anything unexpected
        return True
    return False


def add_flags(df):
    df = df.copy()
    df["read_carefully"] = [needs_review(l, r) for l, r in zip(df["label"], df["rating"])]
    return df


st.set_page_config(page_title=TITLE, layout="wide")
st.title(TITLE)
st.caption(f"Customer feedback for {BUSINESS}. Type a comment, get a label, watch the data grow.")

if using_demo_mode():
    st.warning("No API key found, so the app is using a crude keyword rule instead of an LLM. "
               "Add GROQ_API_KEY to your secrets to use the LLM.")

# Load the data once, then keep it in the session.
if "df" not in st.session_state:
    st.session_state.df = pd.read_csv(CSV_FILE) if os.path.exists(CSV_FILE) else \
        pd.DataFrame(columns=["comment", "rating", "label"])

# ---- 1. Type feedback, get a label, save -----------------------------------
st.subheader("1. Add feedback")
with st.form("feedback_form", clear_on_submit=True):
    comment = st.text_area("Customer comment")
    rating = st.slider("Rating", RATING_MIN, RATING_MAX, 3)
    submitted = st.form_submit_button("Label and save")

if submitted and comment.strip():
    with st.spinner("Labeling..."):
        label = label_comment(comment.strip())
    new_row = pd.DataFrame([{"comment": comment.strip(), "rating": rating, "label": label}])
    st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
    st.session_state.df.to_csv(CSV_FILE, index=False)   # save to CSV
    st.success(f"Label: {label}")

df = add_flags(st.session_state.df)

# ---- 2. Counts and average rating ------------------------------------------
st.subheader("2. What are customers saying?")
left, right = st.columns(2)
with left:
    st.caption("Number of comments per label")
    st.bar_chart(df["label"].value_counts())
with right:
    st.caption("Average rating per label")
    avg = df.groupby("label")["rating"].mean().round(2)
    st.bar_chart(avg)
    st.dataframe(avg.rename("average rating"))

# ---- 3. Read these carefully -----------------------------------------------
st.subheader("3. Read these carefully")
st.caption("The label and the rating disagree (positive with a low rating, negative with a high rating), "
           "or the label is unclear.")
flagged = df[df["read_carefully"]]
if flagged.empty:
    st.info("Nothing flagged.")
else:
    st.dataframe(flagged[["comment", "rating", "label"]], width="stretch")

# ---- All data --------------------------------------------------------------
with st.expander("All feedback"):
    st.dataframe(df, width="stretch")
st.download_button("Download CSV", df.drop(columns="read_carefully").to_csv(index=False),
                   file_name="feedback.csv", mime="text/csv")
st.caption("Note: on the free Streamlit Cloud, the saved file can disappear when the app restarts. "
           "Download your CSV to keep it.")
