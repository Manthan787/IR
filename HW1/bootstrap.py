import Document.Parser
import Document.Indexer
import Query.Parser
import Query.Processor

#Get data from the files and parse them
parsed_docs = Document.Parser.parse_all(Document.Parser.CORPUS_PATH)

# Now Index them!
Document.Indexer.index(parsed_docs)
