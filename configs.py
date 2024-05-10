colors = {
    'region_transmembranaire': 'red',
    'region_de_surface': 'green',
    'region_alpha_helice': 'indigo',
    'region_antigenic': 'yellow',

    'Kyte_Doolittle_scale': 'skyblue',
    'Hopp_Woods_scale': 'wheat',
    'Cornette_scale': 'mistyrose',
    '0': 'blue'
}

#detect, min, max, tolerance
detections = {'region_transmembranaire': [False, 18, 22, 0], #if the values calculated are above 1.6
              'region_de_surface': [False, 5, 8, 0],
              'region_antigenic': [False, 5, 8, 0], #change
              'region_alpha_helice': [False, 5, 8, 0]} 
