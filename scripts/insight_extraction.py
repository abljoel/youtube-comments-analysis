#!/usr/bin/env python
"""Insight Extraction Module"""
import warnings
from pathlib import Path
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
from sklearn.preprocessing import MinMaxScaler
import click

warnings.filterwarnings("ignore")
np.set_printoptions(precision=4)
sns.set_theme()
logging.basicConfig(level=logging.INFO)

CURRENT_DIR = Path()


def save_sentiment_ratio(df, fname, viewer=None):
    """Graph a pie chart of sentiment categories"""
    if viewer:
        plt.title(f"Ratio Chart of {viewer} Sentiments")
    else:
        plt.title("Ratio Chart of Sentiments")
    df["sent_class"].value_counts(normalize=True).plot.pie(autopct="%1.0f%%")
    plt.savefig(CURRENT_DIR / fname)
    logging.info(f"Saved sentiment ratio chart to {CURRENT_DIR / fname}")


def save_top_viewer(df, fname):
    top_viewer = df["author"].describe()["top"]
    top_viewer_data = df[df["author"] == top_viewer]
    save_sentiment_ratio(top_viewer_data, fname, viewer=top_viewer)


def save_top_topics(df, n_viewers, fname):
    n_commenters = int(n_viewers)
    top_n_commenters_content = (
        df.sort_values(by="likes", ascending=False).head(n_commenters).lemmatized_text
    )
    top_terms = "".join([item for item in top_n_commenters_content])
    stopword_list = set(STOPWORDS)

    word_cloud = WordCloud(
        width=550,
        height=550,
        background_color="white",
        stopwords=stopword_list,
        min_font_size=10,
    ).generate(top_terms)

    plt.figure(figsize=(10, 8))
    plt.title(f"WordCloud of Top {n_commenters} Liked Comments")
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.savefig(CURRENT_DIR / fname)
    logging.info(
        f"Saved word cloud of top {n_commenters} liked comments to {CURRENT_DIR / fname}"
    )


def save_engagement_curve(df, fname):
    corpus = df.copy()
    corpus.published_at = pd.to_datetime(corpus.published_at)
    n_comments_over_time = corpus.groupby(corpus["published_at"].dt.date).agg(
        {"likes": "sum", "published_at": "size"}
    )
    scaler = MinMaxScaler()
    normalized_comments_over_time = n_comments_over_time.copy()
    normalized_comments_over_time[["published_at", "likes"]] = scaler.fit_transform(
        normalized_comments_over_time
    )
    plt.figure(figsize=(10, 5))
    plt.plot(
        normalized_comments_over_time.index,
        normalized_comments_over_time.published_at,
        marker="o",
        linestyle="-",
        color="b",
        label="Comments",
    )
    plt.plot(
        normalized_comments_over_time.index,
        normalized_comments_over_time.likes,
        marker="+",
        linestyle="-",
        color="r",
        label="Likes",
    )
    plt.title("Engagement Curve")
    plt.xlabel("Months")
    plt.ylabel("Number of Likes and Comments")
    plt.legend()
    plt.grid(True)
    plt.savefig(CURRENT_DIR / fname)
    logging.info(f"Saved engagement curve to {CURRENT_DIR / fname}")


@click.command()
@click.option(
    "--sentiment",
    is_flag=True,
    help="Plot Ratio of sentiments",
)
@click.option(
    "--top_viewer",
    is_flag=True,
    help="Output top viewer sentiment",
)
@click.option(
    "--top_topics",
    type=str,
    help="Display word cloud of most frequent terms",
)
@click.option(
    "--engagement",
    is_flag=True,
    help="Plot Engagement curve",
)
@click.option(
    "--input_file",
    type=str,
    help="Input file path for loading corpus data",
    required=True,
)
@click.option(
    "--output_file",
    type=str,
    help="Output file path for saving plots",
    required=True,
)
def main(sentiment, top_viewer, top_topics, engagement, input_file, output_file):
    corpus = pd.read_pickle(CURRENT_DIR / input_file)
    try:
        if sentiment:
            save_sentiment_ratio(corpus, output_file)
        if top_viewer:
            save_top_viewer(corpus, output_file)
        if top_topics:
            save_top_topics(corpus, top_topics, output_file)
        if engagement:
            save_engagement_curve(corpus, output_file)
    except Exception as e:
        logging.exception(f"An error occurred during plotting: {e}")


if __name__ == "__main__":
    main()
