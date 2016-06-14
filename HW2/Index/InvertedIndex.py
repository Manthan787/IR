from os.path import join
from Encoder import DeltaEncoder
import uuid
import os
from Catalog import Catalog
from collections import OrderedDict
import sys
index_path = '/Users/admin/Documents/CS6200/HW2/Index/Indices/'

class InvertedIndexWriter( object ):

    def __init__(self, tokens, catalog, name):
        self.tokens     = tokens # tokens with inv_list
        self.catalog    = catalog # Catalog.Catalog object
        self.name       = name  # Name of the index


    def write(self, encode=True):
        path = join(index_path, self.name)
        with open(path, 'w') as f:
            line_number = 1
            prev_end_offset = 0
            for term_id, lst in self.tokens.iteritems():
                inverted_list = "{}\t".format(str(term_id))
                sorted_dIDs   = sorted(lst, key=lambda k: len(lst[k]), reverse=True)

                for docID in sorted_dIDs:
                    if encode:
                        d = DeltaEncoder.encode(lst[docID])
                    else:
                        d = lst[docID]
                    inverted_list += "{}#{}$".format(str(docID), d)

                inverted_list += "\n"
                start_offset  = prev_end_offset
                f.write(inverted_list)
                prev_end_offset = end_offset = f.tell()
                self.catalog.add(term_id, (start_offset, end_offset, line_number))
                line_number += 1
        return self.catalog



class InvertedIndexReader( object ):

    def __init__(self, catalog, path = index_path):
        self.catalog = catalog # Catalog for look-up of offsets
        self.path    = path


    def read(self, term_id):
        path    = join(self.path, self.catalog.name)
        offsets = self.catalog.get_offsets(term_id)
        with open(path, 'r+') as f:
            f.seek(offsets[0])
            return f.read(offsets[1] - offsets[0])


    def readAsDict(self, term_id):
        line = self.read(term_id)
        docs_dict = {}
        term_id, docs = line.split('\t')
        doc_positions = docs.split('$')[0:-1]
        for pos in doc_positions:
            doc_id, positions = pos.split('#')
            lst_pos = map(int, positions[1:-1].split(','))
            docs_dict[doc_id] = lst_pos

        return docs_dict

class InvertedIndexMerger( object ):

    def __init__(self, catalog1, catalog2):
        self.catalog1   = catalog1
        self.catalog2   = catalog2


    def merge(self):
        print "Merging files"
        merge_file = 'M{}'.format(str(uuid.uuid4()).split('-')[-1])
        merge_catalog = Catalog(merge_file)
        merged_tokens = {}


        reader1 = InvertedIndexReader(self.catalog1)
        reader2 = InvertedIndexReader(self.catalog2)
        catalog1_dict = self.catalog1.get()
        catalog2_dict = self.catalog2.get()

        for term_id, offsets in catalog1_dict.iteritems():
            if term_id in catalog2_dict:
                positions_catalog1 = reader1.readAsDict(term_id)
                positions_catalog2 = reader2.readAsDict(term_id)
                positions_catalog1.update(positions_catalog2)
                merged_tokens[term_id] = positions_catalog1
                self.catalog2.delete(term_id)

            else:
                merged_tokens[term_id] = reader1.readAsDict(term_id)

        for term_id, offsets in catalog2_dict.iteritems():
            merged_tokens[term_id] = reader2.readAsDict(term_id)


        merge_writer = InvertedIndexWriter(merged_tokens, merge_catalog, merge_file)
        merge_writer.write(encode=False)
        print "Merging done!"
        return merge_catalog
