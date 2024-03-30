from scales import *
import matplotlib.pyplot as plt
from pdb_to_seq import pdb2seq
#from interface import detections

SCALE = "Kyte_Doolittle_scale"
scale = scales[SCALE]


def calculate_score(seq, score):
    seq_score = []
    for aa in seq:
        seq_score.append(scale[aa])
    return seq_score

def calculate_regions(seq_score):
    r_transmb = []
    r_surface = []

    etat = 0 #1-hydrophob 2-surface

    debut = 0
    fin = 0

    for i in range(len(seq_score)):
        if seq_score[i] > 0 and etat != 1:
            if fin-debut > 3 and fin-debut < 10: r_surface.append((debut, fin))
            debut = i
            etat = 1
        elif seq_score[i] > 0 and etat == 1:
            fin = i
        elif seq_score[i] < 0 and etat != 2:
            if fin-debut > 15 and fin-debut < 25: r_transmb.append((debut, fin))
            debut = i
            etat = 2
        else:
            fin = i
        
    if fin-debut > 3 and fin-debut < 10 and etat == 2:
        r_surface.append((debut, fin))
    elif fin-debut > 15 and fin-debut < 25 and etat == 1:
        r_transmb.append((debut, fin))

    return r_transmb, r_surface


def make_plot(seq, score, debut, fin):
    seq_score = calculate_score(seq, score)
    r_transmb, r_surface = calculate_regions(seq_score)
    seq_nb = [i for i in range(debut, fin)]

    plt.figure().set_figwidth(20)
    plt.clf()

    plt.title("Profile d'hydrophobicite")
    plt.plot(seq_nb, seq_score)
    for region in r_transmb:
        plt.plot(seq_nb[region[0]: region[1]], seq_score[region[0]: region[1]], color = 'red')
    for region in r_surface:
        plt.plot(seq_nb[region[0]: region[1]], seq_score[region[0]: region[1]], color = 'green')
    
    #plt.xlim(debut, fin)
    
    if len(seq) <= 60:
        ticks = [f'{aa}\n{nb}' for aa, nb in zip(seq, seq_nb) ]
        plt.xticks(seq_nb, ticks)

    #print(r_transmb, r_surface)
    plt.show()
    return plt

def analyse(scale, sequ_path, debut, fin):
    seq = pdb2seq(sequ_path)
    if debut != '' and fin != '':
        debut = int(debut)
        fin = int(fin)
        seq = seq[debut: fin]
        plot = make_plot(seq, scale, debut, fin)
    else:
        plot = make_plot(seq, scale, 0, len(seq))
    return plot

if __name__ == '__main__':
    #seq = 'AQPKIVLIVLIVLIVLVLIVLIVLIVLAQPAQPAVLIVVLIVQQQPAQPALLLLQQQQP'
    seq = 'MDFCLLNEKSQIFVHAEPYAVSDYVNQYVGTHSIRLPKGGRPAGRLHHRIFGCLDLCRISYGGSVRVISPGLETCYHLQIILKGHCLWRGHGQEHYFAPGELLLLNPDDQADLTYSEDCEKFIVKLPSVVLDRACSDNNWHKPREGIRFAARHNLQQLDGFINLLGLVCDEAEHTKSMPRVQEHYAGIIASKLLEMLGSNVSREIFSKGNPSFERVVQFIEENLKRNISLERLAELAMMSPRSLYNLFEKHAGTTPKNYIRNRKLESIRACLNDPSANVRSITEIALDYGFLHLGRFAENYRSAFGELPSDTLRQCKKEVA'
    make_plot(seq[5: 10], None, 5, 10)


