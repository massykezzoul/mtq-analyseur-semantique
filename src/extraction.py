import re
import os
import pickle
from bs4 import BeautifulSoup
import requests

# Prend le  mot et retourne grace au  code html correspondant depuis http://www.jeuxdemots.org/rezo-dump et on prendant pour l'instant la relation r_pos telque son poid avec le noeud du mot recercher est maximale.

def extraction_jdm(word: str,rel: str='4'):

    chemin_absolu = os.path.dirname(os.path.abspath(__file__))
    
    if ( os.path.isdir(chemin_absolu + '/cache') and os.path.isfile(
            chemin_absolu + '/cache/' + word + '.pkl')):
        fichier = open(chemin_absolu + '/cache/' + word + '.pkl', 'rb')
        categorie = pickle.load(fichier)
        fichier.close()
        return categorie
    
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

    
    chemin_absolu = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isdir(chemin_absolu + '/cache'):
        try:
            os.mkdir(chemin_absolu + '/cache')
        except OSError:
            print('La cr??ation du dossier cache a ??chou??')
                
    fichier_cache = open(chemin_absolu + '/cache/' + word + '.pkl', 'wb')
    pickle.dump(categorie, fichier_cache)
    fichier_cache.close()
        
    return categorie

def get_pos(categorie):
    tabPOS = ["Adv", "Adj", "Conj", "Det", "Nom", "Pre", "Pro", "Ver","Punct"]

    maxi = 0
    categorie_new = [] 
    for x in categorie:
        element = x[0].split(':')[0]
        if element in tabPOS:
            maxi = 0
            for cat in categorie:
                if element in cat[0] and cat[1] > maxi:
                    maxi = cat[1]
        
            if element not in [y[0] for y in categorie_new]:
                categorie_new.append((element, maxi))
            else:
                for i in range(len(categorie_new)):
                    if element == categorie_new[i][0]:
                        categorie_new[i] = (element, maxi)

    return categorie_new

if __name__ == '__main__':
    phrase = input("Entrez la phrase : \n")
    words = phrase.split(" ")
    for word in words:
        print(get_pos(extraction_jdm(word)))
                
