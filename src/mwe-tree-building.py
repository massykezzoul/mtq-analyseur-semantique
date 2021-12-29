import json

from tqdm import tqdm # progres bar

filename='../jdm/JDM-LEXICALNET-FR/ENTRIES-MWE.txt'

def clean_str(str):
    return str.replace('"', '').strip().split(';')[1].lower()

# À partir du fichier des entrées, on crée un arbre de mots
def build_mwe_tree_dict(filename):
    with open(filename, 'r',encoding='iso-8859-1') as f:
        mwe_list = f.readlines()

    mwe_list = [clean_str(x) for x in mwe_list if not x.strip().startswith('//') and not x.strip() == '']
    mwe_tree = {}

    for mwe in tqdm(mwe_list):
        pointeur = mwe_tree
        phrase = mwe.split(' ')
        i = 0
        while i < len(phrase) and phrase[i] in pointeur:
            pointeur = pointeur[phrase[i]]
            i += 1
        
        if i < len(phrase):
            const = {}
            for word in reversed(phrase[i+1:]):
                const = {word : const}
            pointeur[phrase[i]] = const
        
    return mwe_tree 

tree = build_mwe_tree_dict(filename)

print("Tree built successfully.")

json_file='../data/mwe-tree.json'
with open(json_file, 'w', encoding='iso-8859-1') as f:
    json.dump(tree, f)

print(f"Result writen to {json_file}.")

