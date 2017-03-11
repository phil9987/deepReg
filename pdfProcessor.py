import PyPDF2 as pypdf
import nltk
import operator
from nltk.corpus import stopwords
from nltk.probability import FreqDist


def getCleanString(doc):
    stop_set = set(stopwords.words('english'))
    tokens = nltk.WordPunctTokenizer().tokenize(doc)
    clean = [token.lower() for token in tokens if token.lower() not in stop_set and len(token) > 2 and token.isalpha()]
    return clean


def getPdfTextTokens(filename):
    pdfFileObj = open(filename, 'rb')
    pdfReader = pypdf.PdfFileReader(pdfFileObj)
    text = ""
    for i in range(0, pdfReader.numPages):
        pageObj = pdfReader.getPage(i)
        text += pageObj.extractText()
    pdfFileObj.close()
    return getCleanString(text)


def getTopics(tokens):
    frequencyDistribution = FreqDist(tokens)
    return sorted(frequencyDistribution.items(), key=operator.itemgetter(1))


def main():
    tokens = getPdfTextTokens('./RegulatoryData/596-2014 MAR_Regulations.pdf')
    freqdist = getTopics(tokens)
    for (k, v) in freqdist:
        print(k)
        print v

if __name__ == "__main__":
    main()
