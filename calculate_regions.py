from scales import *
import matplotlib.pyplot as plt
from pdb_to_seq import pdb2seq
from configs import colors

"""Analyse de la sequence"""

def calculate_score(seq, echelle):
    """Calcule le score suivant l'echelle selectionnee
    pour chaque AA de la sequence"""
    seq_scores = {}
    for s in list(echelle.keys()):
        if echelle[s].get():
            seq_scores[s] = []
            for aa in seq:
                #scales[s][0][aa] = score de l'aa donne
                #scales[s][2] = score "neutre" de l'echelle
                #scales[s][0][aa]-scales[s][2] = score normaliser pour que score neutre = 0
                seq_scores[s].append(scales[s][0][aa]-scales[s][2])
    return seq_scores

def score_more(score):
    if score >= 0:
        return True
    return False

def score_less(score):
    if score <= 0:
        return True
    return False

def transmembrane_region(score, param):
    """Cherche des regions transmembranaires"""
    region = []

    #param[1] = taille minimale de la region
    #param[2] = taille maximale de la region
    #param[3] = taux de tolerance de mistakes

    etat = 0 #flag
    debut = 0 #debut de la region
    seuil = 1.6*(1-float(param[3].get()))
    minsize = int(param[1].get())

    i = 0
    while i < len(score)-minsize:
        if etat == 0: 
            debut = i #selection du aa de debut
            somme = sum(score[i:i+minsize])
            if somme/minsize >= seuil: #si la moyenne supperieure au seuil
                i += minsize-1 
                etat = 1 #la region est transmembranaire
                continue
        if etat == 1:
            dist = abs(i-debut)+1 #longeur de la region
            somme += score[i]
            moyenne = somme/dist
            #tant que la taille de la region reste inferieur a la taille maximale
            # et tant que la moyenne est supperieur au seuil
            #la region est aggrandie
            #sinon elle est sauvegardee
            if  not (moyenne >= seuil and dist <= int(param[2].get()) and i<len(score)) :
                    region.append((debut, i))
                    i -= 1
                    etat = 0
        i += 1

    return region


def calculate_regions(score, param, fun):
    """Cherche des regions selectionnes"""
    region = []

    #param[1] = taille minimale de la region
    #param[2] = taille maximale de la region
    #param[3] = taux de tolerance de mistakes

    etat = 0 #flag
    debut = 0 #debut de la region
    fin = 0 #fin de la region
    mistakes = 0 #aa aui ne respectent pas les contraintes de la region

    i = 0
    while i < len(score):
        if etat == 0: 
            debut = i #selection du aa de debut
            etat = 1
        if etat == 1:
            dist = abs(i-debut)+1 #longeur de la region
            #tant que le regions est moins longue aue la valeur maximal
            if dist < int(param[2].get()): 
                #tant que le nombre de mistakes est moins grand que la valeur de mistaques maximale
                if mistakes/dist <= float(param[3].get()): 
                    #ajouter l'aa dans le region. 
                    #Si aa ne correspond pas a la region incrementer mistakes
                    if not fun(score[i]):
                            mistakes += 1
                else: 
                        etat = 2
            else: 
                etat = 2
        
        if etat == 2:
            fin = i
            dist = abs(fin-debut)-1
            #si la region correspond aux contraintes choisit par l'utilisateur
            if dist >= int(param[1].get()) and dist <= int(param[2].get()):
                #ajouter la region
                region.append((debut, fin))
                # et recommencer la recherche d'autres regions sur le reste de la sequence 
                i -= 1
            else:
                #sinon, recommencer le recherche a aa qui suit le aa de debut
                i = debut
            etat = 0
            mistakes = 0
        i += 1

    dist = abs(fin-debut)-1
    if dist > int(param[1].get()) and dist < int(param[2].get())\
          and etat != 0 and mistakes <= dist*float(param[3].get()):
        region.append((debut, fin))

    return region



def plot_region(scale_name, region_name, fun, seq_scores, params, seq_nb):
    """Dessiner les regions identifiee sur le graphe"""
    seq_score = seq_scores[scale_name]
    if region_name == 'region_transmembranaire':
        region = transmembrane_region(seq_score, params[region_name])
    else:
        region = calculate_regions(seq_score, params[region_name],fun)
    i = 0
    for r in region:
        if fun == score_more:
            fin = r[1]
        else:
            fin = r[1]-1
        if i == 0:
            plt.plot(seq_nb[r[0]: fin], seq_score[r[0]: fin], 
                     color = colors[region_name], label = region_name)
            i = 1  
        else:
            plt.plot(seq_nb[r[0]: fin], seq_score[r[0]: fin], 
                     color = colors[region_name])
    return region


def make_plot(seq, debut, fin, params, echelles):
    """Faire le graphe"""
    seq_scores = calculate_score(seq, echelles) #calculer les echelles selectionnees
    seq_nb = [i for i in range(debut, fin)]

    plt.figure().set_figwidth(10)
    plt.clf()

    #Trace des scores de la sequence
    plt.title("Profile d'hydrophobicite")
    for key, item in seq_scores.items():
        plt.plot(seq_nb, item, color = colors[key], label = key)
    
    #Identification des regions selectionnees
    params_keys = []
    for k in list(params.keys()):
        if params[k][0].get():
            params_keys.append(k)
    

    regions = {}
    #Trace des regions trouvees sur le plot
    if 'region_transmembranaire' in params_keys:
        regions['region_transmembranaire'] = plot_region('Kyte_Doolittle_scale', 'region_transmembranaire', 
                                                         score_more, seq_scores, params, seq_nb)
    if 'region_de_surface' in params_keys:
        regions['region_de_surface'] = plot_region('Kyte_Doolittle_scale', 'region_de_surface', 
                    score_less, seq_scores, params, seq_nb)
    if 'region_antigenique_Hoop' in params_keys:
        regions['region_antigenique_Hoop'] = plot_region('Hopp_Woods_scale', 'region_antigenique_Hoop', 
                    score_less, seq_scores, params, seq_nb)
    if 'region_antigenique_Kolaskar' in params_keys:
        regions['region_antigenique_Kolaskar']= plot_region('Kolaskar_Tongaonkar_scale', 'region_antigenique_Kolaskar', 
                    score_more, seq_scores, params, seq_nb)

    #Ajout du nom des aa a l'axe x si la longeur de la sequence <= 60 aa
    if len(seq) <= 60:
        ticks = [f'{aa}\n{nb}' for aa, nb in zip(seq, seq_nb) ]
        plt.xticks(seq_nb, ticks)
    
    plt.plot(seq_nb, [0]*len(seq), color = colors['zero'], label = 'reference')
    #legende.append('reference')

    #legende
    plt.legend(loc = "lower right")

    plt.savefig('plot.png')
    
    return regions


"""Main"""

def analyse(sequ_path, debut, fin, params, echelles): 
    seq = pdb2seq(sequ_path) #Extraction de la sequence du fichier pdb

    #Si zoom sur la sequence particulaire
    if debut != '' and fin != '':
        debut = int(debut)
        fin = int(fin)
        seq = seq[debut: fin]
        regions = make_plot(seq, debut, fin, params,echelles)
    #Si pas de zoom
    else:
        regions = make_plot(seq, 0, len(seq),params, echelles)
    return regions