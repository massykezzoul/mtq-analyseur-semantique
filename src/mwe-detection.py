import json
import networkx as nx

# Cette fonction retourne vrai si la suite de mot est un mot composée (inclus dans l'arbre de mots)
# words : liste de mots
# tree : arbre de mots composés
def is_composed_word(words, tree):
    if words is None or len(words) == 0:
        return False
    if words[0] in tree:
        return is_composed_word(word[:-1], tree[words[0]])
    else:
        return False

# Complète le graph avec les mots composés
def complete_with_composed_words(graph, file_mwe='../data/mwe-tree.json'):
    with open(file_mwe, 'r') as f:
        tree = json.load(f)

    start = '__start__'
    edges = graph.edges(start)
    pass