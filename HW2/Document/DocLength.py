import pickle
from elasticsearch import Elasticsearch

cache_file = "/Users/admin/Documents/CS6200/HW1/Document/doclength.pickle"
INDEX = "ap_dataset"
TYPE = "document"

def cache(docs):
    print "Caching Document Lengths for all the indexed Documents!"
    docLengths = dict()

    for docID in docs:
        es = Elasticsearch()
        res = es.termvectors(index = INDEX, doc_type = TYPE, id = docID,
                             term_statistics = True, positions = True)

        length = 0
        print "%s" %(docID)
        if len(res['term_vectors']) != 0:
            terms = res['term_vectors']['text']['terms']
            for word, stat in terms.iteritems():
                length += stat['term_freq']
        else:
            print "Looks like Document %s is empty! Check it out!" %(docID)

        docLengths[docID] = length

    with open(cache_file, 'wb') as f:
        pickle.dump(docLengths, f)

    print "cached docLength for %s document" %(docID)


def load():
    with open(cache_file, 'rb') as f:
        return pickle.load(f)
