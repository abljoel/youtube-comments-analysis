#!/usr/bin/env python
"""Data Preparation Module"""
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
    df.to_pickle(fdir / fname)
    logging.info(f"Saved the processed corpus to {fdir / fname}")


def read_data(fname, fdir=CURRENT_DIR):
    data = pd.read_csv(fdir / fname)
    return data


def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


def translate_emojis(text):
    tokenized_text = word_tokenize(text)
    for emo in UNICODE_EMOJI:
        if emo in tokenized_text:
            emo_index = tokenized_text.index(emo)
            tokenized_text[emo_index] = (
                UNICODE_EMOJI[emo].replace(":", "").replace("_", " ")
            )
    return " ".join(tokenized_text)


def translate_emoticons(text):
    new_text = text
    for ticon in EMOTICONS_EMO:
        if ticon in new_text:
            new_text = new_text.replace(ticon, EMOTICONS_EMO[ticon])
    return new_text


def filter_text_noise(text):
    next_text = text
    for e in next_text:
        if not e.isalpha():
            next_text = next_text.replace(e, " ")
    return next_text


stop_words = set(stopwords.words("english"))


def filter_stopwords(text):
    stop_words = set(stopwords.words("english"))
    tokenized_text = word_tokenize(text)
    filtered_text = []
    for token in tokenized_text:
        if token not in stop_words:
            filtered_text.append(token)
    return " ".join(filtered_text)


def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    tokenized_text = word_tokenize(text)
    return " ".join([lemmatizer.lemmatize(w) for w in tokenized_text])


def get_sent_label(text="", score=None):
    sent_analyzer = SentimentIntensityAnalyzer()
    if not score:
        score = sent_analyzer.polarity_scores(text)["compound"]
    if 0.4 < score:
        return "positive"
    if -0.1 < score <= 0.4:
        return "neutral"
    return "negative"


def get_sent_score(text):
    sent_analyzer = SentimentIntensityAnalyzer()
    score = sent_analyzer.polarity_scores(text)["compound"]
    return score


def has_emojis(text):
    tokenized_text = word_tokenize(text)
    for emo in UNICODE_EMOJI:
        if emo in tokenized_text:
            return 1
    return 0


def has_emoticons(text):
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
