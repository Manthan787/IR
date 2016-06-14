from os import listdir
from elasticsearch import Elasticsearch, helpers
import pickle
import DocLength


INDEX = 'ap_dataset'
TYPE  = 'document'
# Elasticsearch index settings
ES_SETTINGS = """{
  "settings": {
    "index": {
      "store": {
        "type": "default"
      },
      "max_result_window": 85000,
      "number_of_shards": 1,
      "number_of_replicas": 1
    },
    "analysis": {
      "analyzer": {
        "my_english": {
          "type": "english",
          "stopwords_path": "stoplist.txt"
        }
      }
    }
  },
  "mappings": {
    "document": {
      "properties": {
        "docno": {
          "type": "string",
          "store": true,
          "index": "not_analyzed"
        },
        "text": {
          "type": "string",
          "store": true,
          "index": "analyzed",
          "term_vector": "with_positions_offsets_payloads",
          "analyzer": "my_english"

        }
      }
    }
  }
}
"""


def index(docs):
    """ Indexes the given documents in bulk using Elasticsearch

        Args:
            docs (dict): A dictionary containing all the documents to be indexed

    """
    print "Indexing Documents Using Elasticsearch"
    es = Elasticsearch()
    # Delete index before bulk indexing
    deleteIndex(es)
    # Create new index with given settings
    createIndex(es)
    # Index parsed documents in bulk
    print "Bulk indexing all %s texts" %(len(docs))
    helpers.bulk(es, action(docs))

    # Cache the document lengths of indexed documents for later use
    DocLength.cache(docs)
    
    es.indices.refresh(index = INDEX)
    print es.count(index= INDEX)


def deleteIndex(es):
    """ Deletes the INDEX

        Args:
            es (elasticsearch.client.Elasticsearch'):
                An instance of elasticsearch client

    """
    if es.indices.exists(INDEX):
        print "Deleting '%s' index" % (INDEX)
        response = es.indices.delete(index = INDEX)
        print "Deletion Response %s" %(response)


def createIndex(es):
    """ Creates the INDEX from scratch

        Args:
            es (elasticsearch.client.Elasticsearch'):
                An instance of elasticsearch client

    """
    print "Creating new index from scratch"
    response = es.indices.create(index = INDEX, body = ES_SETTINGS)
    print "Creation Response %s" %(response)


def action(docs):
    """ Generator object for the parsed-document dictionary data
        The bulk-indexer takes this generator object to index the data in bulk
        which is dramatically faster than indexing each document using the
        es.index() method.
    """
    for docno, text in docs.iteritems():
        yield ({'_index': INDEX, '_type': TYPE, '_id':docno,
                '_source': {'docno': docno, 'text': text}})
