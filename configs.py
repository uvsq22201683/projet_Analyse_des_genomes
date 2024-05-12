"""Valeurs de config"""

#info sur des regions a detecter
#detecter la region?, minsize, maxsize, taux de tolerance, seuil de detection
detections = {'region_transmembranaire': [False, 19, 22, 0, 1.6],
              'region_de_surface': [False, 5, 8, 0],
              'region_antigenique_Hoop': [False, 6, 9, 0, 1],
              'region_antigenique_Kolaskar': [False, 6, 20, 0]} 

#couleurs sur le plot
colors = {
    'region_transmembranaire': 'greenyellow',
    'region_de_surface': 'green',
    'region_antigenique_Hoop': 'palegreen',
    'region_antigenique_Kolaskar': 'darkgreen',

    'Kyte_Doolittle_scale': 'blue',
    'Eisenberg_scale': 'deepskyblue',
    'Engelman_scale': 'dodgerblue',

    'Hopp_Woods_scale': 'purple',
    'Kolaskar_Tongaonkar_scale': 'orchid',

    'zero': 'red'
}
