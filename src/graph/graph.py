import networkx as nx

# Function that takes a text and construct a graph
def text_to_graph(text):
    #! TODO: Prétraiter le texte avant de le parser
    #! text = pretraitement(text)
    text_list = text.split()
    graph = nx.Graph()

    # Add nodes to the graph
    for word in text_list:
        graph.add_node(word)

    # Add edges to the graph
    for i in range(len(text_list)-1):
        graph.add_edge(text_list[i], text_list[i+1], weight=1, type='r_succ')
    return graph


if __name__ == '__main__':
    test_text = 'Hello world !'
    graph = text_to_graph(test_text)

    print(f"Nodes: {graph.nodes}")
    print(f"Edges: {graph.edges}")