import tkinter as tk
from calculate_regions import analyse
from configs import detections
from scales import scales
from PIL import Image, ImageTk

"""Creation de Frames"""

def create_frame(texte, x, y, w, h=0.1, py = 10):
    """Creation des frames dans la fenetre principale"""
    frame = tk.LabelFrame(root, background= couleur, text= texte, font=("Robot", 12),
                               width=largeur_ecran*w, height=hauteur_ecran*h, padx= 10, pady=py)
    frame.place(relx = x, rely = y)
    frame.grid_propagate(False)
    frame.pack_propagate(False)
    return frame


def create_sous_frame(s_param, param_name):
    """Creation de frames secondaires pour y entrer des valeurs 
    de traitement des regions dans un frame principale"""

    #creation du sous-frame
    frame = param_frame
    s_frame = tk.Frame(frame, background= couleur,
                               padx = 10, pady = 10)
    s_frame.pack()

    #creation de checkbutton pour selectionner la region a calculer
    val = tk.Variable(frame)
    val.set(0)
    if s_param[0]: #s_param[0] si True: calculer la region
        val.set(1)
    s_param[0] = val
    r = tk.Checkbutton(s_frame, text= param_name, bg = couleur,
                       variable= s_param[0], onvalue = True, offvalue = False,
                       command= change_param_visibility, font=("Robot", 9))
    r.pack()

    #creation de sous frame pour entrez des parametres de la region selectionnee
    ss_frame = tk.Frame(s_frame, background= couleur,
                               padx = 10, pady = 10)
    ss_frame.pack()

    #creation des variables pour selectionner des parametres de la region selectionnee
    s_params = ["valeur minimale", "valeur maximale", "taux de tolerance"]
    for i in range(len(s_params)):
        var = tk.Variable(s_frame)
        var_value = s_param[i+1]
        frame_row(ss_frame, s_params[i], var, var_value, row_nb=i)
        s_param[i+1] = var
    
    # param_frames[nom de la region] : variable qui stoque les 
    # frames responsables pour la region
    param_frames[param_name] = [s_frame, ss_frame]


def frame_row(frame, texte, var, var_value, row_nb, w = 20):
    """Creation d'un champ pour entrer des valeurs"""
    l = tk.Label(frame, text= texte+'  ', font=("Robot", 10),  
                     justify='left', background = couleur, fg = text_couleur)
    l.grid(row = row_nb, column = 0, sticky='w')
    var.set(var_value)
    entry = tk.Entry(frame, textvariable= var, width=w)
    entry.grid(row = row_nb, column = 1)


def place_plot(x, y, path = 'plot.png'):
    """Creation d'une champs pour mettre l'image du plot"""
    image = Image.open(path)
    imgtk = ImageTk.PhotoImage(image)
    l = tk.Label(image=imgtk, text = 'Plot', width=largeur_ecran*0.6, 
                 height=hauteur_ecran*0.53)
    l.image = imgtk
    l.place(relx = x, rely = y)
    


"""Setup les frames"""

def set_path_f(path_frame):
    """Setup le frame pour entrer le chemin du fichier a analyser"""
    frame_row(path_frame, 'Chemin du fichier a analyser:', path, '', 0, 60)

def set_fenetre_f(fenetre_frame):
    """Setup le frame pour zoomer la sequence analysee"""
    frame_row(fenetre_frame, 'Debut:', debut, '', 0) #valeur du debut
    frame_row(fenetre_frame, 'Fin:', fin, '', 1) #valeur de la fin

def set_echelle_f(frame):
    """Setup le frame pour choisir les echelles"""
    scales_name = list(scales.keys()) #ensemble de noms des echelles

    #Variables pour savoir si l'echelle est selectionnee
    for i in scales_name:
        val = tk.Variable(frame)
        val.set(0)
        if i == 'Kyte_Doolittle_scale':
            val.set(1)
        echelles[i] = val 

    #creation de bouttons pour selectionner des echelles
    for s in scales_name:
        r = tk.Checkbutton(frame, text= s, bg = couleur,
                       variable= echelles[s], onvalue = True, offvalue = False, 
                       command= change_scale_visibility, font=("Robot", 9))
        r.pack()

def set_param_f():
    """Setup le frame pour choisir les regions et leur parametres"""
    scales_name = list(scales.keys()) #ensemble de noms des echelles

    for s in scales_name:
        for p in scales[s][1]:
            #creation du sous-frame pour choisir les parametres 
            #pour chaque region
            create_sous_frame(param[p], p)
            param_frames[p][1].forget()
            if not echelles[s].get():
                param_frames[p][0].forget()

def set_region_f(frame, regions, w = 0.55):
    """Setup le afficher des regions identifiees"""

    #Mise en place de l'affichage du texte
    texte = ''
    for key, items in regions.items():
        texte += f'{key} : '
        if len(items) == 0:
            texte += '-\n'
        else:
            for i in range(len(items)):
                texte += f'{items[i]}, '
            texte = texte[:-2]+'\n' 

    #Scrolleur du texte
    s = tk.Scrollbar(frame)
    s.pack(side = 'right', fill = 'y')
    
    l = tk.Text(frame, font=("Robot", 10), background = couleur, fg = text_couleur, 
                     yscrollcommand = s.set, width = int(largeur_ecran*w),
                     highlightthickness=0)
    l.insert('end', texte)
    l.pack(side = 'left', fill = 'y')

    s.config(command=l.yview)
            
            

"""Changement de visibilite des frames"""

def change_param_visibility():
    """Changement de visibilite du frame avec le nom de la region
    Le nom de la region disparait si l'echelle adaptee pour son calcule n'est pas selectionnee
    """
    for p in list(param.keys()):
        try:
            if param[p][0].get():
                param_frames[p][1].pack()
            else:
                param_frames[p][1].forget()
        except AttributeError:
            continue

def change_scale_visibility():
    """Changement de visibilite du frame avec les parametres de la region
    Le frame avec des parametres de la region disparait si la region n'est pas selectionnee
    """
    for s in echelles.keys():
        for p in scales[s][1]:
            if not echelles[s].get():
                param_frames[p][0].forget()
                param_frames[p][1].forget()
                param[p][0].set(False)
            else:
                param_frames[p][0].pack()

"""Main"""

def get_res():
    """Analyse de la sequence proteique"""
    regions = analyse(path.get(), debut.get(), fin.get(), param, echelles) #analyse
    place_plot(0.02, 0.27) #creation du plot
    regions_f = create_frame('Regions localisées', 0.02, 0.8, 0.6, 0.15) #affichage des regions
    set_region_f(regions_f, regions)


def main():
    global root
    global largeur_ecran
    global hauteur_ecran

    global couleur
    global text_couleur

    global path
    global debut
    global fin
    global echelles
    global param
    global param_frames
    global param_frame

    root = tk.Tk()
    
    path = tk.Variable(root) #chemin vers le fichier a analyser
    debut = tk.Variable(root) #zoom debut
    fin = tk.Variable(root) #zoom fin
    echelles = {} #echelles choisies
    param = detections.copy() #parametres des regions
    param_frames = {} #frames des regions

    couleur = '#EFFAF9' #couleur du fond
    text_couleur = 'black' #couleur du texte

    #configuration des la fenetre principale
    root.title('Analyse de genome')
    largeur_ecran = root.winfo_screenwidth()
    hauteur_ecran = root.winfo_screenheight()
    root.geometry(f"{largeur_ecran}x{hauteur_ecran}")
    root.configure(bg = couleur)
    root.resizable(False,False)

    #Mise en page des elements de la fenetre principale
    titre = tk.Label(root, text= 'Logiciel de reconaissance des regions hydrophobes', font=("Robot", 20), 
                     justify='center', background = couleur, fg = text_couleur)
    titre.pack()

    path_frame = create_frame('Fichier  à analyser', 0.02, 0.07, 0.45, py = 20)
    set_path_f(path_frame)

    fenetre_frame = create_frame('Zoom', 0.5, 0.07, 0.15)
    set_fenetre_f(fenetre_frame)

    echelle_frame = create_frame('Echelles',0.67, 0.07, 0.3, 0.25)
    set_echelle_f(echelle_frame)


    param_frame = create_frame('Parametres à determiner', 0.67, 0.25, 0.3, 0.7)
    set_param_f()
    
    analyser_b = tk.Button(text='valider', font=("Robot", 12), width= 20, height= 2,
                           command= get_res)
    analyser_b.place(relx=0.35, rely=0.18)

    root.mainloop()

main()