from graph import graph as g
from extraction import *
from mwe_detection import complete_with_composed_words
import re

if __name__  == "__main__":
    verbose = True
    text = "Le petit chat boit du lait de vache"

    #! prétraitement de la phrase

    # construction du graphe initiale
    graphe = g.text_to_graph(text)

    # Ajout des mots composés
    graphe = complete_with_composed_words(graphe)

    # Ajout des Part Of Speech
    nodes = [e for e in graphe.nodes()]
    for node in nodes:
        if '__start__' in node or '__end__' in node:
            continue

        all_pos = get_pos(extraction_jdm(re.sub(r'\d*#', '',node)))
        for pos in all_pos:
            graphe.add_node(pos[0])
            graphe.add_edge(node, pos[0], type='r_pos', weight=pos[1])

    #! Application des règles

    # affichage du graphe
    g.visualize_graph(graphe, True)

