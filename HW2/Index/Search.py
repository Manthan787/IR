from Catalog import Catalog
from Mapper import Mapper, mappings_path
from InvertedIndex import InvertedIndexReader
from Encoder import DeltaEncoder
import json
from os.path import join

class Search( object ):

    def __init__(self, index):
        self.index = index
        self.__bootstrap()


    def __bootstrap(self):
        self.mapper = Mapper.fromFile(self.index)
        self.catalog = Catalog.fromFile(self.index)        
        self.reader = InvertedIndexReader(self.catalog, '/Users/admin/Documents/CS6200/HW2/Index/Indices/')


    def get_tf(self, term, positions=False):
        try:
            termID = self.mapper.lookupToken(term)
            res = self.reader.readAsDict(termID)
        except ValueError as e:
            return {}
        return self.__construct_doc(res, positions)


    def __construct_doc(self, res_docs, positions):
        docs = {}
        ttf = 0
        docs['df'] = len(res_docs)
        docs['hits'] = {}
        for d, positions in res_docs.iteritems():
            original_docID = self.mapper.reverseLookup(d)
            docs['hits'][original_docID] = {}
            this_doc = docs['hits'][original_docID]
            this_doc['tf'] = len(positions)
            ttf += len(positions)
            if positions:
                this_doc['positions'] = DeltaEncoder.decode(positions)

        docs['ttf'] = ttf
        return docs


    def docLengths(self):
        folder_path = join(mappings_path, self.index)
        print "Loading DocLengths from %s" %folder_path
        path = join(folder_path, 'docLengths')
        with open(path, 'r') as f:
            return json.load(f)


    def sum_ttf(self):
        sum_ttf = 0
        for term in self.catalog.get():
            print "For termID %s" %term
            docs = self.__construct_doc(self.reader.readAsDict(term), positions=False)
            sum_ttf += docs['ttf']

        return sum_ttf

# s = Search('porter2stemstop')
# print s.docLengths()
