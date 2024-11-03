import json
import random
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt

def create_graph(data):
    relationships = []
    for item in data:
        relationships.append((item['business_name'], item['entity']))
    print("Number of edges:", len(relationships))
    
    graph = nx.Graph()
    for a, b in relationships:
        graph.add_edge(a, b)
    print(graph)
    return graph

def plot_graph(graph):
    layout = graphviz_layout(graph, prog = "neato")
    plt.figure(1, figsize=(10, 10))
    conngraph = (
        graph.subgraph(c) for c in nx.connected_components(graph)
    )
    for c in conngraph:
        randomcolor = [random.random()] * nx.number_of_nodes(c)
        nx.draw(c, layout, node_size=40, node_color=randomcolor, vmin=0.0, vmax=1.0, with_labels=False)
            
    plt.title("Graph of Companies and their entities")
    plt.savefig("finalplot.png")
    plt.show()
    plt.close()
    
if __name__ == "__main__":
    with open('./webscraper/NDbusinessdata.json', 'r') as f:
        data = json.load(f)

    network = create_graph(data)
    plot_graph(network) 