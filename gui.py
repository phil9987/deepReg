from appJar import gui
import os
import cPickle as pickle
import PyPDF2 as pypdf
import re


import pdfProcessor
from pdfProcessor import Document

app=gui("Grid Demo","1250x700")

#initialize graph data structure
topic_nodes = []
document_nodes = []
graph_edges = []

def load_all_documents():
    docs = pdfProcessor.loadFromCache()
    for file in os.listdir('./RegulatoryData'):
        if file.endswith('.pdf') and docs.get(file, None) is None:
            pdfFilepath = os.path.join("./RegulatoryData", file)
            new_doc = (Document(pdfFilepath))
            docs[pdfFilepath] = new_doc

            print '.'
            pdfProcessor.save_obj(new_doc.tokens, file)
    return docs

def do_nothing():
    return

def inspect_doc(asd):
    docs = app.getListItems("docs")
    if len(docs)> 0:
        doc = docs[0]
        print "inspect: " + doc

        relevant_topics = []

        for (t,d) in graph_edges:
            if(d == doc):
                print t
                relevant_topics.append(t)

        if not relevant_topics:
            return

        topic_1 = relevant_topics[0]

        text_results = []

        pdfFileObj = open("RegulatoryData/" + doc, 'rb')
        pdfReader = pypdf.PdfFileReader(pdfFileObj)
        text = ""
        for i in range(0, pdfReader.numPages):
            pageObj = pdfReader.getPage(i)
            text = pageObj.extractText()
            #search text for keyword
            index = text.find(topic_1)
            if(index > -1):
                left_border = index-300;
                if(left_border < 0):
                    left_border = 0
                right_border = index+300;
                if(right_border > len(text)):
                    right_border = len(text)
                result_snippet = text[left_border:right_border]

                result_snippet = ' '.join(result_snippet.split())
                result_snippet = re.sub("(.{100})", "\\1\n", result_snippet, 0, re.DOTALL)

                text_results.append(result_snippet)

            if len(text_results) > 30:
                break


        app2=gui()
        app2.setGeometry(700,400)

       

        app2.startPagedWindow(topic_1)

        window_counter = 0
        for res in text_results:
            idstring = "win_id_" + str(window_counter)
            button_id = "button_id_" + str(window_counter)
            window_counter += 1
            app2.startPage()
            res = "..." + res + "..."
            app2.addLabel(idstring, res)
            app2.createRightClickMenu("mymenu"+str(window_counter), showInBar=False)
            app2.addMenuItem("mymenu"+str(window_counter), "Approve", func=None, shortcut=None, underline=-1)
            app2.setLabelRightClick(idstring,"mymenu"+str(window_counter))
            app2.stopPage()

        app2.stopPagedWindow()

        app2.go()

docs = load_all_documents()
print "Docs loaded"

filename_list = []
for (_,d) in docs.iteritems():
    filename_list.append(d.filename)


def save_obj(obj, name):
    with open("temp/" + name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def select_topic(btn):
    topics = app.getListItems("topics")
    if len(topics)> 0:
        print "SEL TOPIC"
        for topic in topics:
            if not topic in topic_nodes:
                topic_nodes.append(topic)

                #for the new topic: find all documents attached to it
                newdocs = pdfProcessor.getAllDocsWithTopic(docs,topic)
                doc_filenames = [d.filename for d in newdocs]

                #check if doc is already present: just add an edge, otherwise also add a node for the doc
                for d in doc_filenames:
                    if not d in document_nodes:
                        document_nodes.append(d)
                    graph_edges.append((topic,d))

    save_obj(topic_nodes,"topic_nodes")
    save_obj(document_nodes,"document_nodes")
    save_obj(graph_edges,"graph_edges")

    #system_call = "python create_graph.py"
    os.system("python create_graph.py")

    app.reloadImage("simple","images/topic_graph.gif")


def compute_common_topics(btn):
	filenames = app.getListItems("docs")
	if len(filenames) > 0:
		print "common topics for: " + str(filenames)

        #
        doc_list = [docs[f] for f in filenames]
        topics = pdfProcessor.getAllCommonTopics(doc_list)
        app.updateListItems("topics", topics)
        

app.setSticky("news")
app.setFont(14)
app.setResizable()

app.startLabelFrame("Hidden Markov Structure Graph", 0, 0,1,3)
app.addImage("simple", "images/start_image.gif")
app.stopLabelFrame()

app.startLabelFrame("Select Topic",0,1,1,1)
app.addEntry("e1")
app.stopLabelFrame()

app.addListBox("topics", ["apple", "orange", "pear", "kiwi"],1,1,1,1)
app.setListBoxMulti("topics");

app.addButton("Select Topic", select_topic,2,1,1,1)

app.addListBox("docs", filename_list,0,2,1,2)
app.setListBoxMulti("docs");

app.addButton("Compute Topics", compute_common_topics,2,2,1,1)

app.setTitle("app_title")

app.createRightClickMenu("mymenu", showInBar=False)
app.addMenuItem("mymenu", "Inspect", func=inspect_doc, shortcut=None, underline=-1)
app.setListBoxRightClick("docs","mymenu")

app.go()