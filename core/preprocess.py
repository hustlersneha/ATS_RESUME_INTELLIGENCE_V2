import string

stopwords = {
    "a", "an", "the", "is", "am", "are", "was", "were",
    "i", "you", "he", "she", "it", "we", "they",
    "to", "of", "and", "in", "on", "for", "with", "at",
    "by", "from", "as", "that", "this", "be", "been", "being"
}

def to_lower(text):
    return text.lower()


def remove_punctuation(text):
    cleaned = ""
    for char in text:
        if char not in string.punctuation:
            cleaned += char
    return cleaned


def tokenize(text):
    return text.split()   # FIX: missing return


def remove_stopwords(tokens):
    filtered = []
    for word in tokens:
        if word not in stopwords:   # FIX: stopwords name corrected
            filtered.append(word)
    return filtered


def preprocess(text):
    text = to_lower(text)
    text = remove_punctuation(text)
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)  # FIX: actually use it
    return tokens