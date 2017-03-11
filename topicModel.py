import pdfProcessor as pp
from pdfProcessor import Document, save_obj
import os
from gensim import corpora, models
from collections import defaultdict
import time

def generateDictionaryAndCorpus():
    frequency = defaultdict(int)
    docs = pp.loadFromCache()
    for file in os.listdir('./RegulatoryData'):
        if file.endswith('.pdf') and docs.get(file, None) is None:
            pdfFilepath = os.path.join("./RegulatoryData", file)
            doc = Document(pdfFilepath)
            docs[doc.filename] = doc
            print '.'
            save_obj(doc.tokens, file)
    docs = [d.tokens for _, d in docs.iteritems()]
    for doc in docs:
        for token in doc:
            frequency[token] += 1
    docs = [[token for token in doc if frequency[token] > 1] for doc in
            docs]  # remove words which only occur in one document
    dictionary = corpora.Dictionary(docs)
    dictionary.save('temp/regulations.dict')
    # print dictionary.token2id
    corpus = [dictionary.doc2bow(doc) for doc in docs]
    corpora.MmCorpus.serialize("temp/regulations.dict", corpus)


def train_model(dict, num_topics, num_passes, update_every, train_corpus, folder, iterations):
    start = time.time()
    lda = models.LdaModel(corpus=train_corpus, id2word=trec_dict, num_topics=num_topics,
                          update_every=update_every, iterations=iterations, passes=num_passes,
                          minimum_probability=0.0, alpha='symmetric')
    corpus_size = len(train_corpus)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    onOffline = 'offline'
    if update_every > 0:
        onOffline = 'online'
    filename = folder + '/lda%iT_%icorpus_%ipasses_' % (num_topics, corpus_size, num_passes) + onOffline + '_' + timestamp
    lda.save(filename)
    logging.info('> model trained in %3.2fs' % (time.time() - start) + 'saved as ' + filename)
    jsd_folder_name = 'lda%iT_%icorpus_' % (num_topics, corpus_size) + onOffline + '_' + timestamp
    return jsd_folder_name, lda

def main():
    frequency = defaultdict(int)
    docs = pp.loadFromCache()
    for file in os.listdir('./RegulatoryData'):
        if file.endswith('.pdf') and docs.get(file, None) is None:
            pdfFilepath = os.path.join("./RegulatoryData", file)
            doc = Document(pdfFilepath)
            docs[doc.filename] = doc
            print '.'
            save_obj(doc.tokens, file)
    docs = [d.tokens for _, d in docs.iteritems()]
    for doc in docs:
        for token in doc:
            frequency[token] += 1
    docs = [[token for token in doc if frequency[token] > 1] for doc in
            docs]  # remove words which only occur in one document
    dictionary = corpora.Dictionary(docs)
    dictionary.save('temp/regulations.dict')
    # print dictionary.token2id
    corpus = [dictionary.doc2bow(doc) for doc in docs]
    corpora.MmCorpus.serialize("temp/regulations.dict", corpus)

    lda = models.LdaModel(corpus, num_topics=30, id2word=dictionary)
    for doc in corpus:
        print lda.get_document_topics(doc)

    print lda.print_topics(30)



if __name__ == "__main__":
    main()