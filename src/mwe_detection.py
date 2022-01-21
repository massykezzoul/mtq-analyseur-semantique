import json
import networkx as nx
from graph import graph as g

# Complète le sous-graph avec les mots composés
def complete_with_composed_words_subgraph(graph, start, subtree, tree, words):
    if '#' in start:
        start_text  = start.split('#')[1]
    else:
        start_text = start

    if start_text in subtree:
        words.append(start)

        # le premier mot est dans les premiers fils de l'arbre des mots composés
        edges = [e for e in graph.edges(start,True)]
        for edge in edges:
            if edge[2]['type'] == 'r_succ':
                if edge[1].split('#')[1] in subtree[start_text]:
                    complete_with_composed_words_subgraph(graph, edge[1], subtree[start_text], tree, words)
                else:
                    if '__end-mwe__' in subtree[start_text] :
                        n = ' '.join(words)

                        graph.add_node(n)

                        for edge in graph.in_edges(words[0],True):
                            if edge[2]['type'] == 'r_succ':
                                graph.add_edge(edge[0], n, type='r_succ', weight=1)

                        for edge in graph.out_edges(words[-1],True):
                            if edge[2]['type'] == 'r_succ':
                                graph.add_edge(n, edge[1], type='r_succ', weight=1)
                        complete_with_composed_words_subgraph(graph, edge[1], tree, tree, [])                
                    else:
                        if len(words) > 1:
                            complete_with_composed_words_subgraph(graph, words[1], tree, tree, [])
                        else:
                            complete_with_composed_words_subgraph(graph, edge[1], tree, tree, [])

                    
    else:
        for edge in graph.edges(start,True):
            if edge[2]['type'] == 'r_succ':
                complete_with_composed_words_subgraph(graph, edge[1], tree, tree, [])
    return

# Complète le graph avec les mots composés
def complete_with_composed_words(graph, file_mwe='../data/mwe-tree.json'):
    with open(file_mwe, 'r') as f:
        tree = json.load(f)

    start = '0#__start__'
    edges = graph.edges(start,True)
    for edge in edges:
        if edge[2]['type'] == 'r_succ':  # A adapter
            complete_with_composed_words_subgraph(graph, edge[1], tree, tree, [])
    return graph

if __name__ == '__main__':
    text = "le petit chat boit du lait de vache"
    graph  = g.text_to_graph(text)

    graph = complete_with_composed_words(graph)
    
    g.visualize_graph(graph)