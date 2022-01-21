import networkx as nx
import matplotlib.pyplot as plt 

import numpy as np
import pylab

def text_to_graph(text):
    #! TODO: Prétraiter le texte avant de le parser
    #! text = pretraitement(text)
    text_list = text.lower().split()
    graph = nx.DiGraph(directed = True)

    # Add nodes to the graph
    graph.add_node('__start__')
    for word in text_list:
        graph.add_node(word)

    # Add edges to the graph
    graph.add_edge('__start__', text_list[0], weight=1, type='r_succ')
    for i in range(len(text_list)-1):
        graph.add_edge(text_list[i], text_list[i+1], weight=1, type='r_succ')
    return graph


if __name__ == '__main__':
    test_text = 'Le chien mange le chat'
    graph = text_to_graph(test_text)

    print(f"Nodes: {graph.nodes}")
       
    
    for edge in graph.edges : 
        print(edge, graph.edges[edge[0],edge[1]]['weight'], graph.edges[edge[0],edge[1]]['type'])
    
    edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in graph.edges(data=True)])
    
    r_succedges = []
    for edge in graph.edges():
        if graph.edges[edge[0],edge[1]]['type'] == 'r_succ': 
            r_succedges.append(edge)
            
    edge_colors = ['black' if not edge in r_succedges else 'red' for edge in graph.edges()]
                
    pos=nx.spring_layout(graph)
    nx.draw_networkx_edge_labels(graph,pos,edge_labels=edge_labels)
    nx.draw_networkx(graph,pos, node_size=1500,edge_color=edge_colors,edge_cmap=plt.cm.Reds)
    pylab.show()
        
    
    
    
    