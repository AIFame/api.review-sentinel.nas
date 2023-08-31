import streamlit as st
import requests
import datetime
from collections import namedtuple
Review = namedtuple('Review', ['text', 'date', 'sentiment', 'votes'])
reviews = []

st.title("Movie Review Sentiment Analyzer")
new_review_text = st.text_input("Enter a movie review: ")
if st.button("Add Review"):
    reviews.append(Review(text=new_review_text, date=datetime.datetime.now(), sentiment=None, votes=0))

for review in reviews:
    if review.sentiment is None:
        response = requests.post(
            "https://api.huggingface.co/analyze",
            headers={"Authorization": "Bearer YOUR_HUGGINGFACE_API_KEY"},
            json={"text": review.text}
        )
        result = response.json()
        # Set thresholds for sentiment classification
        if result['score'] > 0.05:
            sentiment = "Positive"
        elif result['score'] < -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        # Update the review's sentiment
        review = review._replace(sentiment=sentiment)

for review in sorted(reviews, key=lambda r: r.votes, reverse=True):
    st.write(f"Review: {review.text}")
    st.write(f"Date: {review.date}")
    st.write(f"Sentiment: {review.sentiment}")
    st.write(f"Votes: {review.votes}")

    if st.button("Upvote"):
        review = review._replace(votes=review.votes + 1)
    if st.button("Downvote"):
        review = review._replace(votes=review.votes - 1)
