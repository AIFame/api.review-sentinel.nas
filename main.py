import datetime
import os
import uuid
from dataclasses import dataclass
from pprint import pprint
from typing import Final

import cachetools
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from clarifai import Workflow

# Review = namedtuple('Review', ['text', 'date', 'sentiment', 'votes'])

c = cachetools.Cache(maxsize=12)

if 'history' not in st.session_state:
    print('history not found')
    st.session_state.history = c
    c['reviews'] = []
else:
    c = st.session_state.history

reviews = c['reviews']

@dataclass
class Review:
    text: str
    date: str
    sentiment: str
    votes: int


HUGGINGFACE_API_KEY: Final[str] = os.environ['HUGGINGFACE_API_KEY'].strip()

st.title("Movie Review Sentiment Analyzer")
new_review_text = st.text_input("Enter a movie review: ")
if st.button("Add Review"):
    r = Review(text=new_review_text, date=str(datetime.datetime.now()), sentiment='', votes=0)

    reviews.append(r)
    # for i, ri in enumerate(reviews):
    #     st.session_state.history.insert(i, ri)

for review in reviews:
    # ic(review)

    if review.sentiment is None:  # FIXME ==""
        w1 = Workflow('sentiment-analysis')

        eg = [
            {
                "review": f"""This film stands out in today's cinema landscape. Every scene is thoughtfully crafted, and the
        characters have depth and nuance. The story flows naturally, keeping viewers engaged. It's a
        high point in recent movie releases.""".strip(),
                "sentiment": 'positive'
            }
        ]

        res = w1.run(eg[0]["review"])

        outputs = res.results[0].outputs

        pprint(outputs)

        o = outputs[1]
        possible_sentiments = ["Positive", "Negative", "Neutral"]

        print(o)

        sentiment = o.data.text.raw

        for s in possible_sentiments:
            if s.lower() in sentiment.lower():
                sentiment = s
                break

        if sentiment not in possible_sentiments:
            raise ValueError('invalid sentiment')
        # sentiment = sentiment.replace("My answer:","").strip()

        print(f"sentiment is {sentiment}")
        print(f"review is {review}")
        # Update the review's sentiment
        # review._replace(sentiment=sentiment)
        review.sentiment = sentiment

# st.write(reviews)
for i, review in enumerate(reviews):
    print("rvcd rev", review)
    st.write(f"Review: {review.text}")
    st.write(f"Date: {review.date}")
    st.write(f"Sentiment: {review.sentiment}")
    st.write(f"Votes: {review.votes}")

    if st.button("Upvote", key=uuid.uuid4()):
        review.votes += 1
        # review = review._replace(votes=review.votes + 1)
    if st.button("Downvote", key=uuid.uuid4()):
        review.votes -= 1
        # review = review._replace(votes=review.votes - 1)

