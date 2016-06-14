from elasticsearch import Elasticsearch
from HW2.Index.Search import Search

INDEX = "withstopwords"
TYPE  = "document"

s = Search(INDEX)

def all_docs():
    docs = []
    with open('/Users/admin/Documents/CS6200/AP_DATA/doclist.txt') as f:
        for line in f.readlines():
            split_line = line.split(" ")
            if split_line[0] != '0':
                docs.append(split_line[1][:-1])
        return docs


DOCS = all_docs()


def score(queryText, docLength, scoring_function):

    doc_scores = dict()

    for w in queryText:
        print "processing for word %s" %(w)
        documents = s.get_tf(w)
        if len(documents) > 0:
            df = documents['df']
            print "scoring %s documents for the term %s" %(len(documents['hits']), w)
            for docID, val in documents['hits'].iteritems():
                doc = {}
                doc['df'] = df
                doc['tf'] = val['tf']

                if docID in doc_scores.keys():
                    doc_scores[docID] += scoring_function(doc, docLength[docID])
                else:
                    doc_scores[docID] = scoring_function(doc, docLength[docID])
        else:
            print "scoring 0 documents for the term %s" %w
    return doc_scores


def lmScore(queryText, docLength, language_model):
    doc_scores = dict()
    for w in queryText:
        print "Processing for the term %s" %(w)
        documents = s.get_tf(w)
        present_docs = []
        if len(documents) > 0:
            print "Estimating Probabilities for %s present documents" %(len(documents['hits']))
            doc = {'ttf': documents['ttf']}
            for docID, val in documents['hits'].iteritems():
                present_docs.append(docID)
                doc['tf'] = val['tf']
                score = language_model(doc, docLength[docID])
                if docID in doc_scores:
                    doc_scores[docID] += score
                else:
                    doc_scores[docID] = score

            print "Partitioning Documents"
            other_docs = [document for document in DOCS if document not in present_docs]
            print "Estimating Probabilities for absent documents!"
            for document in other_docs:
                docID = document
                doc['tf'] = 0
                score = language_model(doc, docLength[docID])

                if docID in doc_scores:
                    doc_scores[docID] += score
                else:
                    doc_scores[docID] = score

    return doc_scores


def scoreFromCache(queryText, scores):
    doc_scores = dict()
    for w in queryText:
        print "processing for word %s" %(w)
        for docID, score in scores[w].iteritems():
            if docID in doc_scores:
                doc_scores[docID] += score
            else:
                doc_scores[docID] = score

    return doc_scores


def hybrid(queryText, scores, scoring_function, docLength):
    doc_scores = dict()
    for w in queryText:
        print "processing for word %s" %(w)
        if w in scores:
            for docID, score in scores[w].iteritems():
                if docID in doc_scores:
                    doc_scores[docID] += score
                else:
                    doc_scores[docID] = score
        else:
            documents = get_tf(w)
            print "scoring %s documents for the term %s" %(len(documents), w)
            for doc in documents:
                docID = doc['_id']
                if docID in doc_scores.keys():
                    doc_scores[docID] += scoring_function(doc, docLength[docID])
                else:
                    doc_scores[docID] = scoring_function(doc, docLength[docID])

    return doc_scores



def get_tf(term):
    es = Elasticsearch()
    search_body = """
        {{
          "min_score": 1,
          "query": {{
            "function_score": {{
              "query": {{
                "match": {{
                  "text": "{0}"
                }}
              }},
              "functions": [
                {{
                  "script_score": {{
                    "script_id": "getTF",
                    "lang" : "groovy",
                    "params": {{
                      "field": "text",
                      "term": "{0}"
                    }}
                  }}
                }}
              ],
              "boost_mode": "replace"
            }}
          }},
          "script_fields": {{
            "df": {{
              "script": {{
                "inline": "_index[field][term].df()",
                "params": {{
                  "field": "text",
                  "term": "{0}"
                }}
              }}
            }},
            "ttf": {{
              "script": {{
                "inline": "_index[field][term].ttf()",
                "params": {{
                  "field": "text",
                  "term": "{0}"
                }}
              }}
            }}
          }},
          "size": 85000,
          "fields": []
        }}
        """.format(term)

    res = es.search(index = INDEX, doc_type = TYPE, body = search_body)
    if len(res['hits']) > 0:
        return res['hits']['hits']
    else:
        return list()
