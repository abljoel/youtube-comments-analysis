#!/usr/bin/env python
"""
Text Data Processing Module

This module provides functions for processing and preparing text-based data.
It includes functions for cleaning HTML tags, translating emojis and emoticons,
filtering text noise, removing stopwords, lemmatizing text, and performing sentiment analysis.

Functions:
    - save_corpus: Saves a processed DataFrame to a pickle file.
    - read_data: Reads data from a CSV file into a DataFrame.
    - remove_html_tags: Removes HTML tags from text.
    - translate_emojis: Translates Unicode emojis in text.
    - translate_emoticons: Translates emoticons in text.
    - filter_text_noise: Removes non-alphabetic characters from text.
    - filter_stopwords: Removes stopwords from text.
    - lemmatize_text: Lemmatizes words in text.
    - get_sent_label: Returns sentiment label ('positive', 'neutral', 'negative') based on a text's 
      sentiment score.
    - get_sent_score: Returns the sentiment score of a text.
    - has_emojis: Checks if a text contains emojis (returns 1 if true, 0 otherwise).
    - has_emoticons: Checks if a text contains emoticons (returns 1 if true, 0 otherwise).
    - main: Performs data preparation tasks for a text-based DataFrame.

Parameters:
    - input_file (str): Input file path for reading raw data.
    - output_file (str): Output file path for storing processed corpus data.

Note:
    To use the functions in this module, ensure you have the required libraries installed
    (e.g., 'pandas', 'bs4', 'emot', 'nltk') and have the NLTK data downloaded (for stopwords
    and lemmatization).

Usage:
    Run this module as a script to process text-based data and save the processed corpus.
    Command Line Example:
        python your_module_name.py --input_file INPUT_FILE_PATH --output_file OUTPUT_FILE_PATH
"""
import warnings
import logging
from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup
from emot import UNICODE_EMOJI, EMOTICONS_EMO
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import click


warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO)


CURRENT_DIR = Path()


def save_corpus(df, fdir=CURRENT_DIR, fname="corpus.pkl"):
    """Saves a Corpus DataFrame to a pickle file."""
    df.to_pickle(fdir / fname)
    logging.info(f"Saved the processed corpus to {fdir / fname}")


def read_data(fname, fdir=CURRENT_DIR):
    """Reads data from a CSV file into a DataFrame."""
    data = pd.read_csv(fdir / fname)
    return data


def remove_html_tags(text):
    """Removes HTML tags from text."""
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


def translate_emojis(text):
    """Translates Unicode emojis in text."""
    tokenized_text = word_tokenize(text)
    for emo in UNICODE_EMOJI:
        if emo in tokenized_text:
            emo_index = tokenized_text.index(emo)
            tokenized_text[emo_index] = (
                UNICODE_EMOJI[emo].replace(":", "").replace("_", " ")
            )
    return " ".join(tokenized_text)


def translate_emoticons(text):
    """Translates emoticons in text."""
    new_text = text
    for ticon in EMOTICONS_EMO:
        if ticon in new_text:
            new_text = new_text.replace(ticon, EMOTICONS_EMO[ticon])
    return new_text


def filter_text_noise(text):
    """Removes non-alphabetic characters from text."""
    next_text = text
    for e in next_text:
        if not e.isalpha():
            next_text = next_text.replace(e, " ")
    return next_text



def filter_stopwords(text):
    """Removes stopwords from text."""
    stop_words = set(stopwords.words("english"))
    tokenized_text = word_tokenize(text)
    filtered_text = []
    for token in tokenized_text:
        if token not in stop_words:
            filtered_text.append(token)
    return " ".join(filtered_text)


def lemmatize_text(text):
    """Lemmatizes words in text."""
    lemmatizer = WordNetLemmatizer()
    tokenized_text = word_tokenize(text)
    return " ".join([lemmatizer.lemmatize(w) for w in tokenized_text])


def get_sent_label(text="", score=None):
    """
    Returns sentiment label ('positive', 'neutral', 'negative') based on a text's sentiment score.

    Args:
        text (str): The input text for sentiment analysis.
        score (float, optional): The sentiment score of the text. If not provided,
                                  it will be calculated using the SentimentIntensityAnalyzer.

    Returns:
        str: Sentiment label indicating the sentiment of the input text.

    Note:
        The function uses the SentimentIntensityAnalyzer from the nltk library
        to calculate the sentiment score. If a custom score is not provided,
        the function calculates the score for the input text and categorizes it
        as 'positive', 'neutral', or 'negative' based on predefined thresholds.

    Example:
        >>> get_sent_label("This is a positive statement.")
        'positive'
    """
    sent_analyzer = SentimentIntensityAnalyzer()
    if not score:
        score = sent_analyzer.polarity_scores(text)["compound"]
    if 0.4 < score:
        return "positive"
    if -0.1 < score <= 0.4:
        return "neutral"
    return "negative"


def get_sent_score(text):
    """
    Returns the sentiment score of a text.

    Args:
        text (str): The input text for sentiment analysis.

    Returns:
        float: Sentiment score indicating the overall sentiment of the input text.

    Note:
        The function uses the SentimentIntensityAnalyzer from the nltk library
        to calculate the sentiment score. The score ranges from -1 (most negative)
        to 1 (most positive).

    Example:
        >>> get_sent_score("This is a positive statement.")
        0.6369
    """
    sent_analyzer = SentimentIntensityAnalyzer()
    score = sent_analyzer.polarity_scores(text)["compound"]
    return score


def has_emojis(text):
    """Checks if a text contains emojis (returns 1 if true, 0 otherwise)."""
    tokenized_text = word_tokenize(text)
    for emo in UNICODE_EMOJI:
        if emo in tokenized_text:
            return 1
    return 0


def has_emoticons(text):
    """Checks if a text contains emoticons (returns 1 if true, 0 otherwise)."""
    new_text = text
    for ticon in EMOTICONS_EMO:
        if ticon in new_text:
            return 1
    return 0


@click.command()
@click.option(
    "--input_file",
    type=str,
    help="Input file path for reading raw data",
    required=True,
)
@click.option(
    "--output_file",
    type=str,
    help="Output file path for storing processed corpus data",
    required=True,
)
def main(input_file, output_file):
    """
    Perform data preparation tasks for a text-based DataFrame.

    Parameters:
    - input_file (str): Input file path for reading raw data.
    - output_file (str): Output file path for storing processed corpus data.
    """
    try:
        df = read_data(input_file)
        df["cleaned_text"] = df.text.apply(lambda t: remove_html_tags(t))
        df["cleaned_text"] = df.cleaned_text.apply(lambda t: translate_emojis(t))
        df["cleaned_text"] = df.cleaned_text.apply(lambda t: translate_emoticons(t))
        df["cleaned_text"] = df.cleaned_text.apply(lambda t: filter_text_noise(t))
        df["cleaned_text"] = df.cleaned_text.str.lower()
        df["filtered_text"] = df.cleaned_text.apply(lambda t: filter_stopwords(t))
        df["lemmatized_text"] = df.filtered_text.apply(lambda t: lemmatize_text(t))
        df["has_emojis"] = df.text.apply(lambda t: has_emojis(t))
        df["has_emoticons"] = df.text.apply(lambda t: has_emoticons(t))
        df["sent_class"] = df.cleaned_text.apply(lambda t: get_sent_label(t))
        df["sent_score"] = df.cleaned_text.apply(lambda t: get_sent_score(t))
        save_corpus(df=df, fname=output_file)
        logging.info("Successfully processed corpus data")
    except Exception as e:
        logging.exception("An error occurred during data collection: %s", e)


if __name__ == "__main__":
    main()
