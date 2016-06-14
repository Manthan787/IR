from __future__ import division
import math
import os
from ..Document.Parser import CORPUS_PATH, get_docs, load_from_cache, parse
from Indexer import Indexer
from InvertedIndex import InvertedIndexMerger, InvertedIndexReader
import timeit
import Catalog
from Mapper import Mapper, mappings_path
import json
import sys
from threading import Thread

MERGE_SIZE = 2
threads = []


class Batcher(object):

    def __init__(self, size, name):
        self.size       = size
        self.catalogs   = {}
        self.docLengths = {}
        self.name       = name


    def run(self):
        global threads
        docs    = get_docs(CORPUS_PATH)
        mapper  = Mapper()
        i = 1

        for files in self.__chunk(docs):
            doc_contents = []
            for f in files:
                with open(f, 'r') as d:
                    doc_contents.append(d.read())

            doc_contents = ''.join(doc_contents)
            self.__run_batch(parse(doc_contents), i, mapper)
            i += 1

        print "Writing the mapper to file -------------------------------------"
        mapper.write(self.name)
        print "Writing DocLengths to file --------------------------------------"
        self.__writeDocLengths()

        while len(self.catalogs) != 1:
            print self.chunk_catalog()
            for pair in self.chunk_catalog():
                print pair
                if len(pair) != 2:
                    break
                else:
                    cat1 = self.catalogs[pair[0]]
                    cat2 = self.catalogs[pair[1]]
                    self.__merge(cat1, cat2, pair)

        print "Writing the catalog to file for later use -----------------------"
        Catalog.write(self.catalogs, self.name)

    def run_batch(self, docs, batchNo, mapper):
        print "Running Batch %s" %batchNo
        indexer = Indexer(docs, mapper, self.catalogs, self.docLengths)
        indexer.index(keep_stopwords=True, stem=False)


    def __writeDocLengths(self):
        folder_path = os.path.join(mappings_path, self.name)
        path = os.path.join(folder_path, 'docLengths')
        with open(path, 'w') as f:
            json.dump(self.docLengths, f)


    def __merge(self, cat1, cat2, pair):
        merger = InvertedIndexMerger(cat1, cat2)
        merged_cat = merger.merge()
        for p in pair:
            del self.catalogs[p]

        self.catalogs[merged_cat.name] = merged_cat


    def chunk(self, docs):
        ''' Genrator for chunks of files to be processed per batch '''
        for i in range(0, len(docs), self.size):
            yield docs[i : i + self.size]


    def chunk_catalog(self):
        chunks = []
        for i in range(0, len(self.catalogs), 2):
            chunks.append(self.catalogs.keys()[i : i + 2])
        return chunks


    ''' Private Functions '''
    __chunk     = chunk
    __run_batch = run_batch



batcher = Batcher(5, 'withstopwordsDL')
batcher.run()
# print timeit.Timer(batcher.run).timeit(number=1)
