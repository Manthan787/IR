from os import listdir
from os.path import isfile, abspath
import os.path
import re
import pickle


CORPUS_PATH = '/Users/admin/Documents/CS6200/AP_DATA/ap89_collection'
CACHE_PATH  = '/Users/admin/Documents/CS6200/HW1/Document'
parsed_docs_path = os.path.join(CACHE_PATH, 'parsed_docs.pickle')


def get_docs(corpus_path):
    """ returns all the documents to be parsed from the corpus

        Args:
            corpus_path (str) : the path of the corpus

        Returns:
            list : containing the paths of all the files to be parsed from the
                   corpus
    """
    files = []
    # Get the list of all the files in the given corpus_path, remove the readme file
    for f in listdir(corpus_path):
        file_path = os.path.join(corpus_path, f)
        if isfile(file_path) and f != 'readme' and not f.startswith('.'):
            files.append(file_path)

    return files


def parse(docContents):
    ''' Parses the given docuement

        Args:
            docContents (str) : the content of the document to be parsed

        Returns:
            dict: containing docno of each text in the document as key, and the
                  the text as its value
    '''
    # All the parsed documents from the given doc file with <DOCNO> as key and
    # <TEXT> as its value
    docs = dict()

    # Look for the <DOC> .... </DOC> and get the contents between those tags
    docPattern  = re.compile('<DOC>(.+?)</DOC>', re.DOTALL)
    matched_docs = docPattern.findall(docContents)


    # Find the DocNO and Text of each <DOC> in the given Document
    idPattern = re.compile('<DOCNO>(.*?)</DOCNO>', re.DOTALL)
    TextPattern = re.compile('<TEXT>(.*?)</TEXT>', re.DOTALL)

    for document in matched_docs:
        docNo = idPattern.findall(document)
        text  = TextPattern.findall(document)
        docNo = docNo[0].strip()
        text  = preprocess(text)

        docs[docNo] = text

    return docs


def preprocess(text):
    if len(text) > 1:
        text = ''.join(t for t in text)
    else:
        text = text[0]
    return text.strip()


def parse_file(doc):
    ''' Parses the given docuement

        Args:
            doc (str) : the name of the document to be parsed

        Returns:
            dict: containing docno of each text in the document as key, and the
                  the text as its value
    '''
    path = os.path.join(CORPUS_PATH, doc)
    f = open(doc, 'r')
    docContents = f.read()
    f.close()

    return parse(docContents)


def parse_all(corpus):
    """ Parses multiple documents

        Args:
            corpus (str) : the path of the corpus

        Returns:
            dict: containing docno of each text in the document as key, and the
                  the text as its value
    """
    if 'parsed_docs.pickle' in listdir(CACHE_PATH):
        parsed_docs = load_from_cache()
    else:
        print "Could not find documents in cache!"
        print "Collecting files from the corpus ..."
        files = get_docs(CORPUS_PATH)
        print "%s files found" %(len(files))

        contents = ''

        for f in files:
            f_ptr = open(f, 'r')
            contents += f_ptr.read()
            f_ptr.close()

        print "Digging for the texts, yo! ..."
        parsed_docs = parse(contents)
        print "%s texts collected from %s files" %(len(parsed_docs), len(files))
        cache(parsed_docs)
    return parsed_docs


def cache(parsed_data):
    print "Caching data in a pickle file!"
    with open(parsed_docs_path, 'wb') as f_handle:
        pickle.dump(parsed_data, f_handle)
    print "DONE"


def load_from_cache():
    print "Loading parsed documents from cache"
    with open(parsed_docs_path, 'rb') as f_handle:
        parsed_docs = pickle.load(f_handle)
    print "Successfully loaded %s texts from cache" %(len(parsed_docs))
    return parsed_docs
