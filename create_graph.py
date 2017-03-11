import networkx as nx
import matplotlib.pyplot as plt
import cPickle as pickle

from PIL import Image

def create_graph_image(topics,documents,edges):
	G=nx.Graph()

	G.add_nodes_from(topics)
	G.add_nodes_from(documents)
	G.add_edges_from(edges)

	nx.draw_networkx_nodes(G,pos=nx.circular_layout(G),nodelist=topics,node_color='b',node_shape='s',node_size=800,alpha=0.5)
	nx.draw_networkx_nodes(G,pos=nx.circular_layout(G),nodelist=documents,node_color='r',node_size=800,alpha=0.5)
	nx.draw_networkx_labels(G,pos=nx.circular_layout(G))
	nx.draw_networkx_edges(G,pos=nx.circular_layout(G),style="dotted",width=0.3)

	fig1 = plt.gcf()
	axes = plt.gca()
	axes.set_xlim([-1.5,1.5])
	#fig1.add_axes(ax)
	#plt.show()
	plt.draw()
	plt.axis('off')
	#fig1.tight_layout()
	fig1.savefig("images/topic_graph.png",bbox_inches="tight",pad_inches=0)

	im = Image.open("images/topic_graph.png")
	im.save("images/topic_graph.gif")
	



def load_obj(name):
    with open("temp/" + name, 'rb') as f:
		return pickle.load(f)

topic_nodes = load_obj("topic_nodes.pkl")
document_nodes = load_obj("document_nodes.pkl")
graph_edges = load_obj("graph_edges.pkl")
create_graph_image(topic_nodes,document_nodes,graph_edges)