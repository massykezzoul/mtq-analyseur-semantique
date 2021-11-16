# mtq-analyseur-semantique

## Prise en main 

### Dépendances python

Il faut commencer par installer les différentes bibliothèques utilisées dans nos sources. Ces bibliothèques sont listées dans le fichier [requirements.txt](./requirements.txt).

```Shell
    pip install -r requirements.txt
```

### Géneration du graphe

pour générer un graph d'exemple

```Shell
    python src/graph/graph.py
```

## Sujet du projet

Le projet vise à programmer un **[analyseur sémantique](https://fr.wikipedia.org/wiki/Analyse_s%C3%A9mantique)** (simple) de textes français. L'analyse sera **une structure de graphe** calculée à partir du texte et sur laquelle on pourra **extraire des relations sémantiques**. Les relations sémantiques typiques sont celles que l'on peut trouver dans [JDM](http://www.jeuxdemots.org/jdm-about.php). L'implémentation se fera en Python.

## Les tâches

### Réalistion du graphe de travail

Le texte est d'abord transformé en une chaîne linéaire de mots relié par une relation *r_succ.* Des **traitements** (que vous devez préciser) vont rajouter des **nœuds** et des **arc** à ce graphe. 

Les arcs sont des relations **typées, orientées** et **pondérées**. Un poids peut être négatif. Les nœuds portent **une chaîne de caractère** et **un poids.**

Toutes les informations nécessaires doivent être représentées dans le graphe.

Quand vous parcourez votre graphe, le comportement par défaut est de ne pas considérer les nœuds et les relations à poids négatifs. Ainsi, vous gardez dans la structure des solutions envisagées mais finalement rejetées. Il ne faut pas supprimer ces nœuds, mais les négativer.

### Trouver les **termes** composés

Il s'agit de trouver les **termes composés** composant le texte. JDM fournit un grand nombre de termes composés (appelé aussi multi-mots (**MWE**)) . Il faut lire le fichier `LEXICALNET-JEUXDEMOTS-ENTRIES-MWE.txt`, et en faire un arbre préfixe de mots. Ensuite, parcourir le graphe de travail est rajouter les noeuds pour les **MWE** reconnus.

### Définition d'un ensemble de règles

Ces règles permettrons de complèter le graphe de travail pour y ajouter des informations complèmentaire utiles à l'analyse sémantique. Voici un exemple de règle : 

`$x == GN & $y == GV & $x r_succ $y ⇒ $x r_agent-1 $y & $y r_agent $x`

une règle a une **partie gauche** qui est une conjonction de conditions à vérifier dans le graphe, et **une partie droite** qui sont des actions à réaliser (des relations ou des nœuds à ajouter).

### Implèmentation du moteur de règle

Implèmenter le **moteur de règles**, qui prend l'ensemble de règles pour les exécuter. L'algo le plus basique est d'exécuter toutes les règles dans l'ordre, et de recommencer tant que  le graphe est modifié (dans l'esprit  d'un [algorithme de Markov](https://fr.wikipedia.org/wiki/Algorithme_de_Markov)).

### Désambiguïsation des termes

Il faut, dans les cas oû c'est possible, **désambiguïser les termes** ([désambiguïsation lexicale](https://fr.wikipedia.org/wiki/D%C3%A9sambigu%C3%AFsation_lexicale)) qui ont plusieurs sens. Les sens disponibles sont ceux de JDM.

Si vous avez par exemple **A R B**, et que **A** est un terme ayant plusieurs sens, cherchez dans JDM le **A>x** tel que **A>x R B** existe.

Désambiguïser un terme c'est choisir le sens le plus probable dans l'inventair des sens (toujours dans JDM, relation de type 1 :  `r_raff_sem`).

### Résolution des anaphores simples

Un [anaphores](https://fr.wikipedia.org/wiki/Anaphore_(grammaire)) est un mot qui fait réferences à un agent cité précédemment dans la phrase. L'approche est sensiblement la même que pour la *désambiguïsation lexicale*, à savoir chercher dans JDM entre les références possibles, lequels est la plus susceptible d'être l'agent de l'anaphore en qustion. Il y a des anaphores avec les pronom (il, elle, etc), les adjectifs possessifs (son, sa, etc.) et dans de nombreux autres cas à determiner.

### Résultat finale

À la fin de l'analyse, l'objectif est d'avoir des relations sémantiques pour chaque mot composant le texte ainsi que les relations entre les mots. Exemple de résultat :

```markdown
chat r_agent-1 boire
petit chat r_agent-1 boire

boire r_patient lait
boire r_patient lait de chèvre

petit chat r_agent-1 ( boire r_patient lait )
petit chat r_agent-1 ( boire r_patient lait de chèvre )
```

### Visualisation du graphe

Pour la partie visualisation du graphe, l'outil [BRAT](http://brat.nlplab.org/) peut-être utilisé.

Pensez à outiller le système :

- Combien de temps prennent les règles pour être évaluées ?
- Qu'est-ce qui prend du temps ?

Le système doit être le plus rapide possible afin de gérer les textes de grandes tailles, donc essayez d'optimiser ce qui peut l'être. N'oubliez pas que des caches peuvent aider.

### Phase de test

Tester le systeme sur des phrases et paragraphe issus de : 

[Vingt mille lieues sous les mers/Texte entier - Wikisource](https://fr.wikisource.org/wiki/Vingt_mille_lieues_sous_les_mers/Texte_entier)