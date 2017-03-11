import pdfProcessor as pp
from pdfProcessor import Document, save_obj
import os
from gensim import corpora, models


def main():
    docs = pp.loadFromCache()
    for file in os.listdir('./RegulatoryData'):
        if file.endswith('.pdf') and docs.get(file, None) is None:
            pdfFilepath = os.path.join("./RegulatoryData", file)
            doc = Document(pdfFilepath)
            docs[doc.] = doc
            print '.'
            save_obj(doc, file)

    docs = [d.tokens for _, d in docs.iteritems()]

    for doc in docs:
        print doc

if __name__ == "__main__":
    main()