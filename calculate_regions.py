from scales import *
import matplotlib.pyplot as plt
from pdb_to_seq import pdb2seq
#from interface import detections
from configs import colors

SCALE = "Kyte_Doolittle_scale"
scale = scales[SCALE][0]


def calculate_score(seq, echelle):
    seq_scores = {}
    for s in list(echelle.keys()):
        if echelle[s].get():
            seq_scores[s] = []
            for aa in seq:
                seq_scores[s].append(scales[s][0][aa])
    return seq_scores

def score_more(score):
    if score >= 0:
        return True
    return False

def score_less(score):
    if score <= 0:
        return True
    return False

def check_region_general(score, region, fun, i):
    if fun(score[i]):
        region[1][-1].append(i)
        region[0] += 1
        return True
    return False

def check_hydrophobicity(score, region, fun, i):
    if not check_region_general(score, region, fun, i):
        if len(region[1][-1]) == 1:
            del region[1][-1]
            del region[2][-1]
            if len(region[1]) == 0:
                    region[1].append([i])
                    region[2].append([score[i]])
        elif len(region[1][-1])!=0:
            region[1].append([i])
            region[2].append([score[i]])


def check_region(score, region, param, fun, i):
    if not check_region_general(score, region, fun, i):
        print('CCCCCC', region[1], param)
        if len(region[1][-1]) > param[1].get() and \
          len(region[1][-1]) < param[2].get(): # and \
          #(region[0]/len(region[1][-1])) > param[3].get():
            region[0] = 0
            region[1].append([i])
            region[2].append([score[i]])
        else:
            if len(region[1][-1])>0 and i != len(score)-1:
                del region[1][-1]
                del region[2][-1]
                if len(region[1]) == 0:
                    region[1].append([i])
                    region[2].append([score[i]])




def calculate_regions(score, param, fun):

    region = []

    etat = 0
    debut = 0
    fin = 0
    mistakes = 0
    mistake_position = 0

    i = 0
    while i < len(score):
        #if fun(score[i]) and etat == 0:
        if etat == 0:
            debut = i
            etat = 1
            print('D', debut)
        if etat == 1:
            dist = abs(i-debut)+1
            #if dist < int(param[2].get()):
            #print(mistakes/dist, float(param[3].get()), mistakes/dist < float(param[3].get()))
            if dist < int(param[2].get()):
                """if mistakes/dist < float(param[3].get()) and dist < int(param[2].get()):
                        if not fun(score[i]):
                            mistakes += 1
                else: 
                        etat = 2
                    #i -= 1"""
                if mistakes/dist <= float(param[3].get()):
                    if not fun(score[i]):
                            mistakes += 1
                else: 
                        etat = 2
                    #i -= 1"""
            else: 
                etat = 2
        
        if etat == 2: #etat==1:
            fin = i
            dist = abs(fin-debut)
            #if mistakes > dist*int(param[3].get()):
            #    print(mistakes, mistake_position, dist*int(param[3].get()))
            #    i = mistake_position
            if dist >= int(param[1].get()) and dist <= int(param[2].get()):
                #print(mistakes)
                region.append((debut, fin))
                print('F', fin)
                i -= 1
            #elif mistakes> 0:
            #    i = mistake_position-1
            else:
                print(dist, int(param[1].get()),int(param[2].get()) )
                i = debut
            etat = 0
            mistakes = 0
        i += 1

    dist = abs(fin-debut-1)    
    if dist > int(param[1].get()) and dist < int(param[2].get())\
          and etat != 0 and mistakes <= dist*float(param[3].get()):
        region.append((debut, fin))

    print(region)
    return region


def make_plot(seq, debut, fin, params, echelles):
    seq_scores = calculate_score(seq, echelles)
    #regions = calculate_regions(seq_score, params)
    #r_transmb, r_surface = calculate_regions1(seq_score)
    seq_nb = [i for i in range(debut, fin)]

    plt.figure().set_figwidth(10)
    plt.clf()

    plt.title("Profile d'hydrophobicite")
    for key, item in seq_scores.items():
        plt.plot(seq_nb, item, color = colors[key])
    
    params_keys = []
    for k in list(params.keys()):
        if params[k][0].get():
            params_keys.append(k)
    if 'region_transmembranaire' in params_keys:
        seq_score = seq_scores['Kyte_Doolittle_scale']
        region = calculate_regions(seq_score, params['region_transmembranaire'], score_more)
        for r in region:
            plt.plot(seq_nb[r[0]: r[1]], seq_score[r[0]: r[1]], color = colors['region_transmembranaire'])
    if 'region_de_surface' in params_keys:
        seq_score = seq_scores['Kyte_Doolittle_scale']
        region = calculate_regions(seq_score, params['region_de_surface'], score_less)
        for r in region:
            plt.plot(seq_nb[r[0]: r[1]-1], seq_score[r[0]: r[1]-1], color = colors['region_de_surface'])
    """if 'region_alpha_helice' in params_keys:
        calculate_regions(seq_scores['Kyte_Doolittle_scale'], params['Kyte_Doolittle_scale'], score_more)
    if 'region_antigenic' in params_keys:
        calculate_regions(seq_scores['Kyte_Doolittle_scale'], params['Kyte_Doolittle_scale'], score_more)"""

    
    #plt.plot(regions[region][1][i], regions[region][2][i], color = colors[region])
    
    #plt.xlim(debut, fin)
    
    if len(seq) <= 60:
        ticks = [f'{aa}\n{nb}' for aa, nb in zip(seq, seq_nb) ]
        plt.xticks(seq_nb, ticks)

    #print(r_transmb, r_surface)
    #plt.show()
    plt.savefig('plot.png')
    return plt

def analyse(sequ_path, debut, fin, params, echelles): #+scale
    seq = pdb2seq(sequ_path)
    if debut != '' and fin != '':
        debut = int(debut)
        fin = int(fin)
        seq = seq[debut: fin]
        plot = make_plot(seq, debut, fin, params,echelles)
        
    else:
        plot = make_plot(seq, 0, len(seq),params, echelles)
        
    return plot