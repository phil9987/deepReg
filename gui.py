from appJar import gui
import os
import cPickle as pickle

app=gui("Grid Demo","1250x700")

#initialize graph data structure
topic_nodes = ["NODE1","NODE2"]
document_nodes = ["DOC1"]
graph_edges = []

def save_obj(obj, name):
    with open("temp/" + name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def select_topic(btn):
    items = app.getListItems("topics")
    if len(items)> 0:
        print "SEL TOPIC"

    save_obj(topic_nodes,"topic_nodes")
    save_obj(document_nodes,"document_nodes")
    save_obj(graph_edges,"graph_edges")

    #system_call = "python create_graph.py"
    os.system("python create_graph.py")

    app.setImage("simple","images/topic_graph.gif")


def compute_common_topics(btn):
	items = app.getListItems("docs")
	if len(items) > 0:
		print "COMMON TOPICS"

app.setSticky("news")
app.setFont(14)
app.setResizable()

app.startLabelFrame("Hidden Markov Structure Graph", 0, 0,1,3)
app.addImage("simple", "images/start_image.png")
app.stopLabelFrame()

app.startLabelFrame("Select Topic",0,1,1,1)
app.addEntry("e1")
app.stopLabelFrame()

app.addListBox("topics", ["apple", "orange", "pear", "kiwi"],1,1,1,1)
app.setListBoxMulti("topics");

app.addButton("Select Topic", select_topic,2,1,1,1)

app.addListBox("docs", ["apple", "orange", "pear"],0,2,1,2)
app.setListBoxMulti("docs");

app.addButton("Compute Topics", compute_common_topics,2,2,1,1)

app.setTitle("app_title")

app.go()