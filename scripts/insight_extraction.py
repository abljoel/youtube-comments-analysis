#!/usr/bin/env python
"""
Insight Extraction Script

This module provides functions for information extraction throught data visualization,
including sentiment proportion charts, top viewer sentiment extraction, word cloud generation
for top commenters, and engagement curve plotting.

Functions:
    - save_sentiment_ratio: Graphs a pie chart of sentiment categories.
    - save_top_viewer: Extracts and saves data related to the top viewer from the given DataFrame.
    - save_topics_from_top_viewers: Generates and saves a word cloud representing common topics
                                    in the comments from the top N liked commenters.
    - save_engagement_curve: Generates and saves an engagement curve, plotting the number of likes
                             and comments over time.
    - main: Main function to generate and save visualizations based on user input options.

Usage:
    # Example: Execute script to generate visualizations based on user input options
    python insight_extraction.py --sentiment --output_file "opinions_pie.png"
"""

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
    """
    Extracts and saves data related to the top viewer from the given DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame containing viewer data.
        fname (str): The output file name for saving the data.

    Note:
        The function calculates the top viewer based on the 'author' column in the DataFrame.
        It then extracts data related to the top viewer and saves the sentiment ratio using
        the 'save_sentiment_ratio' function.
    """
    top_viewer = df["author"].describe()["top"]
    top_viewer_data = df[df["author"] == top_viewer]
    save_sentiment_ratio(top_viewer_data, fname, viewer=top_viewer)


def save_topics_from_top_viewers(df, n_viewers, fname):
    """
    Generates and saves a word cloud representing the common topics in the comments
    from the top N liked commenters in the given DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame containing comments data.
        n_viewers (int): The number of top commenters whose comments will be considered.
        fname (str): The output file name for saving the word cloud image.

    Returns:
        None

    Note:
        The function extracts the lemmatized text from the top N liked commenters
        based on the number of likes in the DataFrame. It then generates a word cloud
        visualization using the 'WordCloud' library and saves the image file.
    """
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
    """
    Generates and saves an engagement curve, plotting the number of likes and comments over time.

    Args:
        df (pandas.DataFrame): The input DataFrame containing comments data with a
        'published_at'column.
        fname (str): The output file name for saving the engagement curve plot.

    Returns:
        None

    Note:
        The function converts the 'published_at' column to datetime format and groups the
        data by date.
        It then calculates the sum of likes and the total number of comments for each date.
        The engagement values are normalized using MinMaxScaler and plotted over time.
    """
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
    "--top_viewer_topics",
    type=str,
    help="Display wordcloud of most frequent terms for top N viewers",
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
def main(sentiment, top_viewer, top_viewer_topics, engagement, input_file, output_file):
    """
    Main function to generate and save visualizations based on user input options.

    Args:
        sentiment (bool): If True, plot Ratio of sentiments.
        top_viewer (bool): If True, output top viewer sentiment.
        top_viewer_topics (str): Number of top viewers for displaying wordcloud of
                                 most frequent terms.
        engagement (bool): If True, plot Engagement curve.
        input_file (str): Input file path for loading corpus data.
        output_file (str): Output file path for saving plots.

    Returns:
        None

    Note:
        The function reads a corpus DataFrame from a pickle file and generates visualizations
        based on the specified options. It uses functions like 'save_sentiment_ratio',
        'save_top_viewer', 'save_topics_from_top_viewers', and 'save_engagement_curve'.
    """
    corpus = pd.read_pickle(CURRENT_DIR / input_file)
    try:
        if sentiment:
            save_sentiment_ratio(corpus, output_file)
        if top_viewer:
            save_top_viewer(corpus, output_file)
        if top_viewer_topics:
            save_topics_from_top_viewers(corpus, top_viewer_topics, output_file)
        if engagement:
            save_engagement_curve(corpus, output_file)
    except Exception as e:
        logging.exception(f"An error occurred during plotting: {e}")


if __name__ == "__main__":
    main()
