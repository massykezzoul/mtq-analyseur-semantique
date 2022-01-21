import json
import networkx as nx

# Cette fonction retourne vrai si la suite de mots est un mot composée (inclus dans l'arbre de mots)
# words : liste de mots
# tree : arbre de mots composés
def is_composed_word(words, tree):
    if words is None or len(words) == 0:
        return False
    if words[0] in tree:
        return is_composed_word(word[:-1], tree[words[0]])
    else:
        return False

# Complète le sous-graph avec les mots composés
def complete_with_composed_words_subgraph(start, tree, words=[]):
    if start in tree:
        # le premier mot est dans les premiers fils de l'arbre des mots composés
        for edge in graph.edges(start):
            if type(edge) == 'r_succ':
                if edge[1] in tree[start]:
                    complete_with_composed_words_subgraph(edge[1], tree[start], words.append(start))
                elif len(tree[start].keys()) == 0:
                    graph.add_edge(start, edge[1], type='r_succ') ## Ajouter le mot composé dans le graph
    else:
        for edge in graph.edges(start):
            if type(edge) == 'r_succ':
                complete_with_composed_words_subgraph(edge[1], tree)
    return

# Complète le graph avec les mots composés
def complete_with_composed_words(graph, file_mwe='../data/mwe-tree.json'):
    with open(file_mwe, 'r') as f:
        tree = json.load(f)

    start = '__start__'
    edges = graph.edges(start)
    for edge in edges:
        if type(edge) == 'r_succ':  # A adapter
            complete_with_composed_words_subgraph(edge[1], tree)
    return