from __future__ import division
from Query.RetrievalModels import unigramLaplace, get_tf, all_docs, okapiTF, okapiBM25, tfidf
from Query.Parser import get_queries, queries_file
import Document.DocLength
import math
import sys
import pickle


DOCS = all_docs()

def generateScoresLM(scoring_func):
    queries = get_queries(queries_file)
    print "Loading Document Lengths from cache ..."
    docLength = Document.DocLength.load()
    print "Successfully Loaded DocLengths from cache!"
    print "------------------------------------------"
    scores = dict()
    for qID, query in queries.iteritems():
        for w in query:
            if w not in scores:
                print "Processing for the term %s" %(w)
                documents = get_tf(w)
                print "Scoring %s present documents" %(len(documents))
                present_docs = []
                scores[w] = dict()
                for doc in documents:
                    docID = doc['_id']
                    present_docs.append(docID)
                    tf = doc['_score']
                    scores[w][docID] = scoring_func(tf, docLength[docID])

                print "Partitioning Documents"
                other_docs = [doc for doc in DOCS if doc not in present_docs]
                print "Scoring absent documents"
                for doc in other_docs:
                    tf = 0
                    docID = doc
                    scores[w][docID] = scoring_func(tf, docLength[docID])

    return scores


def generateScoresVSM(scoring_func):
    queries = get_queries(queries_file)
    print "Loading Document Lengths from cache ..."
    docLength = Document.DocLength.load()
    print "Successfully Loaded DocLengths from cache!"
    print "------------------------------------------"
    scores = dict()

    for qID, query in queries.iteritems():
        for w in query:
            if w not in scores:
                print "processing for word %s" %(w)
                documents = get_tf(w)
                print "scoring %s documents for the term %s" %(len(documents), w)
                scores[w] = dict()

                for doc in documents:
                    docID = doc['_id']
                    scores[w][docID] = scoring_func(doc, docLength[docID])

    return scores

def cacheLM():
    scores = generateScoresLM(unigramLaplace)
    print "Caching scores!"
    with open('/Users/admin/Documents/CS6200/HW1/Query/LaplaceCache.pickle', 'wb') as f:
        pickle.dump(scores, f)
    print "Done!"


def cacheVSM():
    scores = generateScoresVSM(tfidf)
    print "Caching scores!"
    with open('/Users/admin/Documents/CS6200/HW1/Query/TFIDFCache.pickle', 'wb') as f:
        pickle.dump(scores, f)
    print "Done!"

cacheVSM()
