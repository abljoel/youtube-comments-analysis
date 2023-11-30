from bs4 import BeautifulSoup
from emot import UNICODE_EMOJI, EMOTICONS_EMO
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer


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
