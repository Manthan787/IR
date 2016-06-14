import json
from os.path import join
import os
mappings_path = '/Users/admin/Documents/CS6200/HW2/Mappings/'

class Mapper( object ):

    # docIDMap        = {}
    # dIDReverseMap   = {}
    # tokenMap        = {}
    prevDocID       = 0
    prevTokenID     = 0


    def __init__(self, tokenMap = {}, docIDMap = {}, dIDReverseMap = {}):
        self.tokenMap       = tokenMap
        self.docIDMap       = docIDMap
        self.dIDReverseMap  = dIDReverseMap


    @classmethod
    def fromFile(self, folder):
        print "Getting the mapper ready!"
        tokenpath = construct_path(folder, 'token_Mappings')
        docpath   = construct_path(folder, 'docID_Mappings')
        rdocpath  = construct_path(folder, 'rdocID_Mappings')
        with open(tokenpath, 'r') as t:
            tokenMap = json.load(t)

        with open(docpath, 'r') as d:
            docIDMap = json.load(d)

        with open(rdocpath, 'r') as d:
            dIDReverseMap = json.load(d)


        return self(tokenMap, docIDMap, dIDReverseMap)


    def mapToken(self, token):
        if token in self.tokenMap:
            return self.tokenMap.get(token)
        else:
            self.prevTokenID    += 1
            self.tokenMap[token] = self.prevTokenID
            return self.prevTokenID


    def mapDocID(self, docID):
        if docID in self.docIDMap:
            return self.docIDMap.get(docID)

        else:
            self.prevDocID += 1
            self.docIDMap[docID] = self.prevDocID
            self.dIDReverseMap[self.prevDocID] = docID
            return self.prevDocID


    def lookupToken(self, token):
        if token in self.tokenMap:
            return self.tokenMap.get(token)

        else:
            raise ValueError('The token could not be found in the tokenmap!')


    def lookupDocID(self, docID):
        if docID in self.docIDMap:
            return self.docIDMap.get(docID)

        else:
            raise ValueError('The token could not be found in the tokenmap!')


    def reverseLookup(self, mapped_dID):
        if mapped_dID in self.dIDReverseMap:
            return self.dIDReverseMap.get(mapped_dID)

        else:
            raise ValueError('The token could not be found in the tokenmap!')



    def write(self, path):
        print "Writing Doc ID Mappings to file"
        self.__write_to_file('docID_Mappings', self.docIDMap, path)
        print "Writing Reverse Doc ID Mappings to file"
        self.__write_to_file('rdocID_Mappings', self.dIDReverseMap, path)
        print "Writing Token Mappings to file"
        self.__write_to_file('token_Mappings', self.tokenMap, path)


    def __write_to_file(self, name, data, folder):
        folder_path = join(mappings_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        path = join(folder_path, name)
        with open(path, 'w') as m:
            json.dump(data, m)



def construct_path(folder, name):
    folder_path = join(mappings_path, folder)
    return join(folder_path, name)
