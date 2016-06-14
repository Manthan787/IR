from __future__ import division
import math

avg_doclen = 453
def unigramLaplace(doc, docLength):
    tf = doc['tf']
    # Vocabulary size
    V = 178081
    laplace = (tf + 1) / (docLength + V)
    return math.log(laplace)


def unigramJM(doc, docLength):
    lamb = 0.6
    sum_ttf  = 20984156
    tf = doc['tf']
    ttf = doc['ttf']
    try:
        term1 = lamb * (tf / docLength)
    except ZeroDivisionError as e:
        term1 = 0
    term2 = (1 - lamb) * ((ttf - tf) / (sum_ttf - docLength))
    return math.log(term1 + term2)


# For Personally Built Index
def unigramJM_new(doc, docLength):
    lamb = 0.6
    sum_ttf  = avg_doclen * 84678
    tf = doc['tf']
    ttf = doc['ttf']
    try:
        term1 = lamb * (tf / docLength)
    except ZeroDivisionError as e:
        term1 = 0
    term2 = (1 - lamb) * ((ttf - tf) / (sum_ttf - docLength))
    return math.log(term1 + term2)


def okapiTF(doc, docLength):
    tf = doc['tf']
    nor_length = docLength / avg_doclen
    deno = tf + 0.5 + (1.5 * nor_length)
    return tf / deno


def tfidf(doc, docLength):
    N = 84678
    df = doc['fields']['df'][0]
    rarity = math.log(N / df)
    return okapiTF(doc, docLength) * rarity


# For Personally Built Index
def tfidf_new(doc, docLength):
    N = 84678
    df = doc['df']
    rarity = math.log(N / df)
    return okapiTF(doc, docLength) * rarity


def okapiBM25(doc, docLength):
    df = doc['fields']['df'][0]
    tf = doc['_score']
    nor_length = docLength / 248
    N = 84678
    k1 = 1.2
    b  = 0.75
    term1 = math.log((N + 0.5) / (df + 0.5))
    term2 = (tf + (k1 * tf)) / (tf + k1 * ((1 - b) + (b * nor_length)))
    return term1 * term2


# For Personally Built Index
def okapiBM25_new(doc, docLength):
    df = doc['df']
    tf = doc['tf']
    nor_length = docLength / avg_doclen
    N = 84678
    k1 = 1.2
    b  = 0.75
    term1 = math.log((N + 0.5) / (df + 0.5))
    term2 = (tf + (k1 * tf)) / (tf + k1 * ((1 - b) + (b * nor_length)))
    return term1 * term2
