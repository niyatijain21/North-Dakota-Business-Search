import json
import random
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt

def create_graph(data):
    rows = next(item['rows'] for item in data if 'rows' in item)
    
    relationships = []
    for item in data:
        if 'business_name' in item and 'entity' in item:
            relationships.append((item['business_name'], item['entity']))
    
    graph = nx.Graph()
    for a, b in relationships:
        graph.add_edge(a, b)
    print(graph)
    return graph

def plot_graph_with_info(graph):
    layout = graphviz_layout(graph, prog="neato")
    plt.figure(1, figsize=(10, 10))
    
    # Get connected components
    components = list(nx.connected_components(graph))
    
    # Create a color map to store colors for each component
    color_map = {}
    with open("network_components_info.txt", "w") as f:
        f.write("Network Components Information:\n")
        
        # Process each component
        for idx, component in enumerate(components):
            # Generate a random color for this component
            color = random.random()
            color_map[idx] = color
            
            # Create subgraph for this component
            c = graph.subgraph(component)
            
            # Write component info to file
            f.write(f"\nNetwork Group {idx + 1} (Color Value: {color:.2f}):\n")
            f.write(f"Number of nodes: {len(component)}\n")
            f.write(f"Entities in this network: {sorted(list(component))}\n")
            
            # Draw the component
            nx.draw(c, layout,
                   node_size=40,
                   node_color=[color] * nx.number_of_nodes(c),
                   vmin=0.0,
                   vmax=1.0,
                   with_labels=False)
    plt.title("Graph of Companies and their entities")
    plt.savefig("finalplot.png")
    plt.show()
    plt.close()
    
if __name__ == "__main__":
    with open('./webscraper/NDbusinessesdata.json', 'r') as f:
        data = json.load(f)

    network = create_graph(data)
    plot_graph_with_info(network) 