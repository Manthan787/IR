from __future__ import division
from HW2.Index.Search import Search
from HW1.Query.Parser import get_queries, queries_file
from HW1.Query.Processor import write_to_file
import Minspan
import sys

INDEX = 'porter2stemstop'

s = Search(INDEX)
docLengths = s.docLengths()

queries = get_queries(queries_file)
# queries = {1: ['manufactures', 'pharmaceuticals']}
def search():
    for qID, query in queries.iteritems():
        docs_terms = {}
        for w in query:
            print "Processing for the term %s" %w
            docs = s.get_tf(w, positions=True)
            if len(docs) > 0:
                for dID, pos in docs['hits'].iteritems():
                    if dID in docs_terms:
                        docs_terms[dID][w] = pos['positions']
                    else:
                        docs_terms[dID] = {}
                        docs_terms[dID][w]   = pos['positions']

        res = rank(docs_terms)
        write_to_file(qID, res, 'prox-search')


def rank(docs_terms):
    scores = {}
    for dID, w_pos in docs_terms.iteritems():
        rangeWin = Minspan.rangeWindow(w_pos)
        # print rangeWin
        scores[dID] = proximity_score(rangeWin, len(w_pos), docLengths[dID])

    return scores


def proximity_score(rangeW, containterms, dl):
    C = 1500
    # V = 198588  # nonstemmed, with stop words
    V = 157727 # stemmed, no stopwords
    t1 = (C - rangeW) * containterms
    t2 = dl + V
    return t1 /t2


search()
