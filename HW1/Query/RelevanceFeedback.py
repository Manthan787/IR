from __future__ import division
from Processor import loadDocLengths, loadScores, write_to_file, sort_results
from elasticsearch import Elasticsearch
from Scorers import hybrid
from RetrievalModels import okapiBM25, tfidf, okapiTF
from Parser import get_queries, queries_file
import subprocess
import math
import sys


es = Elasticsearch()
queries = get_queries(queries_file)


def queryVector(query):
    vector = {}
    for w in query:
        if w != ' ':
            vector[w] = 1
    return vector


def relVector(rel_docs):
    relVector = {}
    for doc in rel_docs:
        res = es.termvectors(index = 'ap_dataset', doc_type = 'document', id = doc)
        terms = res['term_vectors']['text']['terms']
        relVector[doc] = terms

    return relVector


def rocchio(qVec, rVec):
    a = 1
    b = 0.8
    Nr = 100
    rVec_sum = vec_sum(rVec)
    for t, val in rVec_sum.iteritems():
        rVec_sum[t] = (b / 100) * val

    new_query = query_rel_sum(qVec, rVec_sum)
    return new_query

def query_rel_sum(qVec, rVec_sum):
    for w, val in qVec.iteritems():
        if w in rVec_sum:
            rVec_sum[w] += val
        else:
            rVec_sum[w]  = val

    return rVec_sum


def vec_sum(vec):
    highest_len = 0
    highest_vec = None
    hID = None
    resultant = {}
    for docID, vector in vec.iteritems():
        if len(vector) > highest_len:
            highest_len = len(vector)
            highest_vec = vector
            hID = docID

    print "Highest Length " + str(highest_len)
    for term, _ in highest_vec.iteritems():
        for docID, vector in vec.iteritems():
            t = vector.get(term, {})
            if term in resultant:
                resultant[term] +=  t.get('term_freq', 0)
            else:
                resultant[term] = t.get('term_freq', 0)

    return resultant


def reRun(qID, query, docLength, scores):
    res = hybrid(query, scores, okapiTF, docLength)
    write_to_file(qID, res, 'feedback-2')


def modify(query, relDocs):
    qV = queryVector(query)
    rV = relVector(relDocs)
    ans = rocchio(qV, rV)
    top = sort_results(ans)[0:10]
    print "original query "
    print query
    l = list(query)
    x = []
    for t in top:
        if t[0] not in query:
            x.append(t[0])

    for term in x[0:2]:
        l.append(term)


    print l
    return l



def select_best(terms, query):
    print "finding best related term for %s" %(terms)
    search_body = get_searchBody(terms)
    res = es.search(index = 'ap_dataset', doc_type = 'document', body = search_body)
    related = res['aggregations']['related']
    sig_terms = related['buckets']
    foreground = related['doc_count']
    sig = {}
    for t in sig_terms:
        key = t['key']
        if key not in query:
            doc_count = t['doc_count']
            bg_count = t['bg_count']
            sig[key] = t['score']

    s_sig = sort_results(sig)
    print "Significant terms ranked"
    print s_sig
    return s_sig[0][0]


def best(sig_scores):
    if len(sig_scores) > 0:
        return sort_results(sig_scores)[0][0]
    else:
        return list()


def calculate_significance(doc_count, bg_count, foreground):
    N = 84678
    t1 = doc_count / foreground
    IDF =  N / bg_count
    if t1 < 0.15:
        return -100

    t2 = doc_count / bg_count
    return math.log(IDF * t1 * t2)


def get_searchBody(term):
        return """{{
            "query" : {{
                "terms" : {{"text" : [ "{0}" ]}}
            }},
            "aggregations" : {{
                "related" : {{
                    "significant_terms" : {{
                      "field" : "text"
                    }}
                }}
            }},
            "size": 0
        }}""".format(term)


def evaluate(name):
    subprocess.call(['../trec_eval', '../AP_DATA/qrels.adhoc.51-100.AP89.txt', 'Results/' + name])


def main():
    docLength = loadDocLengths()
    scores = loadScores('Okapi')
    res = {}
    with open('Results/okapitf-cached', 'r') as f:
        for line in f.readlines():
            splt = line.split(" ")
            qID = splt[0]
            dID = splt[2]
            if qID in res:
                res[qID].append(dID)
            else:
                res[qID] = list()
                res[qID].append(dID)

    # for qID, query in queries.iteritems():
    #     print "Modifying query"
    #     modified_query = modify(queries[qID], res[qID])
    #     print modified_query
    #     reRun(qID, modified_query, docLength, scores)
    #     print "After modifying the query"
    #     evaluate('feedback-2')

    print "Modifying query"
    qID = '63'
    modified_query = modify(queries[qID], res[qID])
    print modified_query
    reRun(qID, modified_query, docLength, scores)
    print "After modifying the query"
    evaluate('feedback-2')


if __name__ == '__main__':
    main()
    #evaluate()
    # select_best('salari')
