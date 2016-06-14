from ..Document.Parser import CORPUS_PATH, get_docs, load_from_cache, parse
from Tokenizer import Tokenizer
from InvertedIndex import InvertedIndexWriter
from Catalog import Catalog
from stemming.porter import stem as porter_stem
from stemming.porter2 import stem as porter2_stem
from nltk.corpus import stopwords
import uuid

stop_words = stopwords.words('english')

class Indexer( object ):

    def __init__(self, docs, mapper, catalogs, docLengths):
        self.docs       = docs
        self.mapper     = mapper
        self.catalogs   = catalogs
        self.docLengths = docLengths


    # Index one incoming batch!
    def index(self, keep_stopwords=True, stem=False):
        print "Indexing %s documents in bulk!" %(len(self.docs))

        inverted_list = {}
        for dID, text in self.docs.iteritems():
            tokenizer = Tokenizer(text)
            tokens = tokenizer.tokenize()
            position = 1
            filtered_tokens = []
            for t in tokens:
                if not keep_stopwords:
                    if t in stop_words:
                        continue

                if stem:
                    t = porter2_stem(t)

                filtered_tokens.append(t)
                mDocID = self.mapper.mapDocID(dID)
                mToken = self.mapper.mapToken(t)
                if mToken not in inverted_list:
                    inverted_list[mToken] = {}

                inverted_list[mToken].setdefault(mDocID, []).append(position)
                position += 1

            self.docLengths[dID] = len(filtered_tokens)

        return self.__writeInvertedIndex(inverted_list)


    def __writeInvertedIndex(self, inverted_list):
        print "Writing inverted index to disk and creating the catalog"
        catalog_name = str(uuid.uuid4()).split('-')[-1]
        catalog = Catalog(catalog_name)
        writer = InvertedIndexWriter(inverted_list, catalog, catalog_name)
        self.catalogs[catalog_name] = writer.write()
