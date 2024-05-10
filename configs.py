colors = {
    'region_transmembranaire': 'red',
    'region_de_surface': 'green',
    'region_antigenic_Hoop': 'indigo',
    'region_antigenic_Kolaskar': 'yellow',

    'Kyte_Doolittle_scale': 'skyblue',
    'Hopp_Woods_scale': 'wheat',
    'Cornette_scale': 'mistyrose',
    'Kolaskar_Tongaonkar_scale': 'plum',


    '0_Kyte': 'blue',
    '0_Hopp': 'goldenrod',
    '0_Cornette': 'firebrick',
    '0_Kolaskar': 'purple',

}

#detect, min, max, tolerance
detections = {'region_transmembranaire': [False, 18, 22, 0], #if the values calculated are above 1.6
              'region_de_surface': [False, 5, 8, 0],
              'region_antigenic_Hoop': [False, 2, 10, 0],
              'region_antigenic_Kolaskar': [False, 6, 20, 0]}
              #'region_alpha_helice': [False, 5, 8, 0]} 
