from scales import *
import matplotlib.pyplot as plt
from pdb_to_seq import pdb2seq
from configs import colors


def calculate_score(seq, echelle):
    seq_scores = {}
    for s in list(echelle.keys()):
        if echelle[s].get():
            seq_scores[s] = []
            for aa in seq:
                seq_scores[s].append(scales[s][0][aa])
    return seq_scores

def score_more(score, value):
    if score >= value:
        return True
    return False

def score_less(score, value):
    if score <= value:
        return True
    return False


def calculate_regions(score, param, fun, value):

    region = []

    etat = 0
    debut = 0
    fin = 0
    mistakes = 0

    i = 0
    while i < len(score):
        if etat == 0:
            debut = i
            etat = 1
        if etat == 1:
            dist = abs(i-debut)+1
            if dist < int(param[2].get()):
                if mistakes/dist <= float(param[3].get()):
                    if not fun(score[i], value):
                            mistakes += 1
                else: 
                        etat = 2
            else: 
                etat = 2
        
        if etat == 2:
            fin = i
            dist = abs(fin-debut)-1
            if dist >= int(param[1].get()) and dist <= int(param[2].get()):
                region.append((debut, fin))
                i -= 1
            else:
                i = debut
            etat = 0
            mistakes = 0
        i += 1

    dist = abs(fin-debut)-1
    if dist > int(param[1].get()) and dist < int(param[2].get())\
          and etat != 0 and mistakes <= dist*float(param[3].get()):
        region.append((debut, fin))

    print('AAAAAAaaaa', region)
    return region

def plot_region(scale_name, region_name, fun, seq_scores, params, seq_nb):
    seq_score = seq_scores[scale_name]
    region = calculate_regions(seq_score, params[region_name], 
                                   fun, scales[scale_name][2])
    for r in region:
        if fun == score_more:
            plt.plot(seq_nb[r[0]: r[1]], seq_score[r[0]: r[1]], color = colors[region_name])
        else:
            plt.plot(seq_nb[r[0]: r[1]-1], seq_score[r[0]: r[1]-1], color = colors[region_name])


def make_plot(seq, debut, fin, params, echelles):
    seq_scores = calculate_score(seq, echelles)
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
        plot_region('Kyte_Doolittle_scale', 'region_transmembranaire', score_more, seq_scores, params, seq_nb)
    if 'region_de_surface' in params_keys:
        plot_region('Kyte_Doolittle_scale', 'region_de_surface', score_less, seq_scores, params, seq_nb)
    if 'region_antigenic_Hoop' in params_keys:
        plot_region('Hopp_Woods_scale', 'region_antigenic_Hoop', score_less, seq_scores, params, seq_nb)
    if 'region_antigenic_Kolaskar' in params_keys:
        plot_region('Kolaskar_Tongaonkar_scale', 'region_antigenic_Kolaskar', score_more, seq_scores, params, seq_nb)

    
    #plt.plot(regions[region][1][i], regions[region][2][i], color = colors[region])
    
    #plt.xlim(debut, fin)
    
    if len(seq) <= 60:
        ticks = [f'{aa}\n{nb}' for aa, nb in zip(seq, seq_nb) ]
        plt.xticks(seq_nb, ticks)

    plt.savefig('plot.png')

def analyse(sequ_path, debut, fin, params, echelles): #+scale
    seq = pdb2seq(sequ_path)
    if debut != '' and fin != '':
        debut = int(debut)
        fin = int(fin)
        seq = seq[debut: fin]
        make_plot(seq, debut, fin, params,echelles)
        
    else:
        make_plot(seq, 0, len(seq),params, echelles)