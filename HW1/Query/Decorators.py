import string
from stemming.porter2 import stem
from nltk.corpus import stopwords
import DependencyParser


def tokenize(get_queries):
    def wrapper(*args, **kwargs):
        queries = get_queries(*args, **kwargs)
        cleaned = cleanUp(queries)
        avoid = list()
        for k, v in cleaned.iteritems():
            # cleaned[k] = v.split(" ")
            cleaned[k] = preprocess_query(v.split(" "), avoid)
        return cleaned
    return wrapper


def cleanUp(queries):
    for k, v in queries.iteritems():
        punctuations = set(string.punctuation)
        v_without_puncts = ""
        for ch in v:
            if ch in punctuations:
                v_without_puncts += ' '
            else:
                v_without_puncts += ch
        queries[k] = v_without_puncts.strip()
    return queries


def preprocess_query(tokens, avoid):
    stop_words = stopwords.words('english')
    stemmed = list()
    for token in tokens:
        if token not in stop_words + avoid:
            # stemmed.append(token.lower())
            stemmed.append(stem(token.lower()))
    return set(stemmed)


def dependency_parse(get_queries):
    def wrapper(*args, **kwargs):
        queries = get_queries(*args, **kwargs)
        cleaned = cleanUp(queries)

        for k, v in cleaned.iteritems():
            avoid = DependencyParser.parse(v)
            avoid.append('Document')
            cleaned[k] = preprocess_query(v.split(" "), avoid)

        return cleaned
    return wrapper
