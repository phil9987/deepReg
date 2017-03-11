from __future__ import division     # needed for integer division with float result
import PyPDF2 as pypdf
import nltk
import operator
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import os
import cPickle as pickle

class Document:
    def __init__(self, filepath, tokens=None):
        self.filepath = filepath
        if(tokens == None):
            self.tokens = self.getPdfTextTokens(filepath)
        else:
            self.tokens = tokens

    def getCleanString(self, doc):
        stop_set = set(stopwords.words('english'))
        tokens = nltk.WordPunctTokenizer().tokenize(doc)
        clean = [token.lower() for token in tokens if token.lower() not in stop_set and len(token) > 2 and token.isalpha()]
        return clean

    def getPdfTextTokens(self, filepath):
        pdfFileObj = open(filepath, 'rb')
        pdfReader = pypdf.PdfFileReader(pdfFileObj)
        text = ""
        for i in range(0, pdfReader.numPages):
            pageObj = pdfReader.getPage(i)
            text += pageObj.extractText()
        pdfFileObj.close()
        return self.getCleanString(text)

    def getTopics(self):
        frequencyDistribution = FreqDist(self.tokens)
        importantTopics = dict(sorted(frequencyDistribution.items(), key=operator.itemgetter(1), reverse=True)[:20])
        total = sum(importantTopics.values())
        topics = {k: v/total for (k, v) in importantTopics.iteritems()}     # get probability of each topic
        return topics


def save_obj(obj, name):
    with open('deepReg/obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('deepReg/obj/' + name, 'rb') as f:
        return pickle.load(f)


def cache_documents(docs):
    for doc in docs:
        save_obj(doc.tokens, doc.filepath.split('/')[-1])
        print '#'


def loadFromCache():
    docs = {}
    for file in os.listdir('./deepReg/obj'):
        if file.endswith('.pkl'):
            pdfFilename = file.partition(".pkl")[0]
            docs[pdfFilename] = Document(os.path.join('./deepReg/RegulatoryData', pdfFilename), load_obj(file))
    return docs


def getAllDocsWithTopic(docs, topic):
    relevantDocs = {}
    for pdfFilepath, doc in docs.iteritems():
        if topic in doc.getTopics().keys():
            relevantDocs[pdfFilepath] = doc
    return relevantDocs


def getAllCommonTopics(docs):
    topics = []
    for pdfFilepath, doc in docs.iteritems():
        topics.append(set(doc.getTopics().keys()))
    return set.intersection(*topics)


def getAllTopics(docs):
    topics = []
    for pdfFilepath, doc in docs.iteritems():
        topics += doc.getTopics().keys()
    return topics


def main():
    docs = loadFromCache()
    for file in os.listdir('./deepReg/RegulatoryData'):
        if file.endswith('.pdf') and docs.get(file, None) is None:
            pdfFilepath = os.path.join("./deepReg/RegulatoryData", file)
            docs[pdfFilepath](Document(pdfFilepath))
            print '.'
            save_obj(docs.pop().tokens, file)
    for filename, doc in docs.iteritems():
        freqdist = doc.getTopics()
        for (k, v) in freqdist.iteritems():
            print k
            print v
    tradingDocs = getAllDocsWithTopic(docs, "trading")
    for pdfFilePath, doc in tradingDocs.iteritems():
        print doc.filepath

    commonTopics = getAllCommonTopics()


if __name__ == "__main__":
    main()
