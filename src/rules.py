
def desambiguisation(rule, graphe):
    gauche = rule.split('=>')[0].strip()
    droite = rule.split('=>')[1].strip()

    pass

def groupage(rule, graphe):
    pass

def inference(rule, graphe):
    pass


def apply_rules(graphe, rule_file):
    with open(rule_file, 'r') as f:
        # read line by line
        lines = f.readlines()
        i=0
        while i < len(lines) and "groupage" not in lines[i]:
            ## désambiguisation
            regle = lines[i].strip()
            if regle != "":
                desambiguisation(regle, graphe)
            i += 1
        while i < len(lines) and "inference" not in lines[i]:
            ## groupage
            regle = lines[i].strip()
            if regle != "":
                groupage(regle, graphe)
            i += 1
        while i < len(lines):
            ## inférence
            regle = lines[i].strip()
            if regle != "":
                inference(regle, graphe)
            i += 1
