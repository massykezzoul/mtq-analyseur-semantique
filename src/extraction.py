import re
from unittest import case
from itertools import groupby
from operator import itemgetter
from bs4 import BeautifulSoup
import requests

# Prend le  mot et retourne grace au  code html correspondant depuis http://www.jeuxdemots.org/rezo-dump et on prendant pour l'instant la relation r_pos telque son poid avec le noeud du mot recercher est maximale.

def extraction(word: str,rel: str='4'):
    html = requests.get('http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=' + word + '&rel='+rel)
    encoding = html.encoding if 'charset' in html.headers.get('content-type', '').lower() else None
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding='iso-8859-1')
    texte_brut = soup.find_all('code')
    noeuds = re.findall('[e];[0-9]*;.*', str(texte_brut))
    relations = re.findall('[r];[0-9]*;.*', str(texte_brut))
    if ((not noeuds) and (not relations)):
        print("le mot " + word + " n'existe pas dans jeux de mots")
        return None
    
    tableau_noeuds = []
    tableau_relations = []

    for noeud in noeuds:
        noeud = noeud.replace('&lt;', '<')
        noeud = noeud.replace('&gt;', '>')
        tableau_noeuds.append(noeud.split(';'))
    for relation in relations:
        relation = relation.replace('&lt;', '<')
        relation = relation.replace('&gt;', '>')
        tableau_relations.append(relation.split(';'))

    id = {}
    i = 0
    while i <= len(tableau_relations) - 1:
        if (int(tableau_relations[i][5]) >= 0):
            id[int(tableau_relations[i][3])] = int(tableau_relations[i][5])
        i += 1

    categorie = []
    for N in tableau_noeuds:
        if (int(N[1]) in id):
            if '>' in N[2] and len(N) >= 6:
                categorie.append((N[5].replace("'", ''), id[int(N[1])]))
            else:
                categorie.append((N[2].replace("'", ''), id[int(N[1])]))

    return categorie


phrase = input("Entrez la phrase : \n")
words = phrase.split(" ")
for word in words:
    if (word[len(word) - 1] in ['.', ',', '!', ':', '?', ';']):
        print(word[:-1] + "  :: ")
        print(extraction(str(word[:-1])))
        print(word[len(word) - 1] + "  :: ")
        print(extraction(str(word[len(word) - 1])))
    else:
        print(word + "  :: ")
        print(extraction(str(word)))
            