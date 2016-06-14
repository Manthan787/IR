from Parser import get_queries, queries_file
from Scorers import score, lmScore, scoreFromCache
from threading import Thread
import RetrievalModels
import pickle
import operator
import sys
from Scorers import INDEX
from HW2.Index.Search import Search


def processAllFromCache(function_name, result_file):
    scores = loadScores(function_name)
    queries = get_queries(queries_file)

    for qID, query in queries.iteritems():
        res = processFromCache(query, scores)
        t = writingThread(res, qID, result_file)

    t.join()


def processAll(scoring_function, model_name, result_file):
    # docLength = loadDocLengths()
    docLength = s.docLengths()
    queries = get_queries(queries_file)

    print "Processing all the queries!"
    for qID, query in queries.iteritems():
        res = process(model_name, query, docLength, scoring_function)
        t = writingThread(res, qID, result_file)

    t.join()


def process(model_name, query_text, docLength, scoring_function):
    if model_name == 'VSM':
        return score(query_text, docLength, scoring_function)
    else:
        return lmScore(query_text, docLength, scoring_function)


def processFromCache(query, scores):
    return scoreFromCache(query, scores)


def loadScores(scoring_function):
    print "Loading Scores from cache ..."
    scores = {}
    cache_file = scoring_function + 'Cache.pickle'
    with open('/Users/admin/Documents/CS6200/HW1/Query/Cache/' + cache_file) as f:
        return pickle.load(f)


def loadDocLengths():
    print "Loading Document Lengths from cache ..."
    with open('/Users/admin/Documents/CS6200/HW1/Document/doclength.pickle') as f:
         return pickle.load(f)


def writingThread(scores, qID, filename):
    print "Starting new thread to write results for query %s" %(qID)
    try:
        t = Thread(None, write_to_file, None, (qID, scores, filename))
        t.start()
        return t
    except Exception as e:
        print e


def write_to_file(queryID, scores, filename):
    sorted_scores = sort_results(scores)
    i = 1
    filename = '/Users/admin/Documents/CS6200/HW1/Query/Results/' + filename
    f = open(filename, 'a')
    for ss in sorted_scores[0:100]:
        line = "{queryNo} Q0 {docNo} {rank} {score} Exp\n".format(queryNo = queryID, docNo = ss[0], rank = i, score = ss[1])
        f.write(line)
        i = i + 1
    f.close()
    print "Results for the query %s successfully written to file!" %(queryID)


def sort_results(scores):
    return sorted(scores.items(), key = operator.itemgetter(1), reverse = True)


def hasCorrectArgs():
    return len(sys.argv) == 4


def hasFlag():
    return sys.argv[1] == '-c'


if __name__ == '__main__':
    if hasCorrectArgs():
        s = Search(INDEX)
        if hasFlag():
            result_file = sys.argv[2]
            scoring_function = sys.argv[3]

            processAllFromCache(scoring_function, result_file)

        else:
            result_file = sys.argv[1]
            model_name  = sys.argv[2]
            scoring_function = sys.argv[3]

            try:
                func = getattr(RetrievalModels, scoring_function)
                processAll(func, model_name, result_file)
            except AttributeError as e:
                print "The scoring function argument can be one of : okapiTF, okapiBM25, tfidf, unigramLaplace or unigramJM"

    else:
        print "Usage: python Processor.py [-c] <result_file_name> <model_name> <scoring_function_name>"
        print "The only allowed flag is -c. Which runs the scoring from the scores stored in cache!"
        print "<model_name> can be either VSM (Vector Space Model) or LM (Language Models)"
        print "<scoring_function_name> is the name of the scoring function to be used for ranking. e.g. okapiTF"
