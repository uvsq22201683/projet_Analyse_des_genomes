import tkinter as tk
from calculate_regions import analyse
from configs import detections
from scales import scales
from PIL import Image, ImageTk

### Frame creation
def create_frame(texte, x, y, w, h=0.1, py = 10):
    frame = tk.LabelFrame(root, background= couleur, text= texte, font=("Robot", 12),
                               width=largeur_ecran*w, height=hauteur_ecran*h, padx= 10, pady=py)
    frame.place(relx = x, rely = y)
    frame.grid_propagate(False)
    frame.pack_propagate(False)
    #frame.grid_columnconfigure(1, weight=3)
    return frame

def create_sous_frame(s_param, param_name):
    frame = param_frame
    s_frame = tk.Frame(frame, background= couleur,
                               padx = 10, pady = 10)
    s_frame.pack()

    val = tk.Variable(frame)
    val.set(0)
    print(s_param)
    if s_param[0]:
        val.set(1)
    s_param[0] = val
    r = tk.Checkbutton(s_frame, text= param_name, bg = couleur,
                       variable= s_param[0], onvalue = True, offvalue = False,
                       command= change_param_visibility, font=("Robot", 9))
    r.pack()
    ss_frame = tk.Frame(s_frame, background= couleur,
                               padx = 10, pady = 10)
    ss_frame.pack()

    s_params = ["valeur minimale", "valeur maximale", "pourcentage de tolerance"]
    for i in range(len(s_params)):
        var = tk.Variable(s_frame)
        var_value = s_param[i+1]
        frame_row(ss_frame, s_params[i], var, var_value, row_nb=i)
        s_param[i+1] = var
    
    param_frames[param_name] = [s_frame, ss_frame]
    print(param_frames, param_name)

def frame_row(frame, texte, var, var_value, row_nb, w = 20):
    l = tk.Label(frame, text= texte+'  ', font=("Robot", 10),  
                     justify='left', background = couleur, fg = text_couleur)
    l.grid(row = row_nb, column = 0, sticky='w')
    #l.pack( side = 'left')
    var.set(var_value)
    entry = tk.Entry(frame, textvariable= var, width=w)
    entry.grid(row = row_nb, column = 1)
    #entry.pack( side = 'left', expand= True,  fill='both')
    

def place_plot(x, y, path = 'plot.png'):
    # Create a photoimage object of the image in the path
    image = Image.open(path)
    imgtk = ImageTk.PhotoImage(image)
    l = tk.Label(image=imgtk, text = 'Plot', width=largeur_ecran*0.6, 
                 height=hauteur_ecran*0.53)
    l.image = imgtk
    l.place(relx = x, rely = y)
    

### set frames
def set_path_f(path_frame):
    frame_row(path_frame, 'Chemin du fichier a analyser:', path, '', 0, 60)

def set_fenetre_f(fenetre_frame):
    frame_row(fenetre_frame, 'Debut:', debut, '', 0)
    frame_row(fenetre_frame, 'Fin:', fin, '', 1) #!!!!!!!!

def set_echelle_f(frame):
    scales_name = list(scales.keys())

    for i in scales_name:
        val = tk.Variable(frame)
        val.set(0)
        if i == 'Kyte_Doolittle_scale':
            val.set(1)
        echelles[i] = val 
    
    for s in scales_name:
        r = tk.Checkbutton(frame, text= s, bg = couleur,
                       variable= echelles[s], onvalue = True, offvalue = False, 
                       command= change_scale_visibility, font=("Robot", 9))
        r.pack()

def set_param_f(frame):
    scales_name = list(scales.keys())

    for s in scales_name:
        for p in scales[s][1]:
            create_sous_frame(param[p], p)
            param_frames[p][1].forget()
            if not echelles[s].get():
                param_frames[p][0].forget()
            
            

### Change visibility

def change_param_visibility():
    for p in list(param.keys()):
        try:
            if param[p][0].get():
                param_frames[p][1].pack()
            else:
                param_frames[p][1].forget()
        except AttributeError:
            continue

def change_scale_visibility():
    for s in echelles.keys():
        for p in scales[s][1]:
            if not echelles[s].get():
                param_frames[p][0].forget()
                param_frames[p][1].forget()
                param[p][0].set(False)
            else:
                param_frames[p][0].pack()

### Main

def get_res():
    analyse(path.get(), debut.get(), fin.get(), param, echelles)
    place_plot(0.02, 0.27)
    regions_f = create_frame('Regions localisées', 0.02, 0.8, 0.6, 0.15)


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
    
    path = tk.Variable(root)
    debut = tk.Variable(root)
    fin = tk.Variable(root)
    echelles = {}
    #param = [[], [], [], []] #selected, frame, var_radio, values of params
    param = detections.copy()
    param_frames = {}

    couleur = '#EFFAF9'
    text_couleur = 'black'

    root.title('Analyse de genome')
    largeur_ecran = root.winfo_screenwidth()
    hauteur_ecran = root.winfo_screenheight()
    root.geometry(f"{largeur_ecran}x{hauteur_ecran}")
    root.configure(bg = couleur)
    root.resizable(False,False)

    titre = tk.Label(root, text= 'Logiciel de reconaissance des regions hydrophobes', font=("Robot", 20), 
                     justify='center', background = couleur, fg = text_couleur)
    #titre.grid(row = 0, column= 1, columnspan= 2)
    titre.pack()

    path_frame = create_frame('Fichier  à analyser', 0.02, 0.07, 0.45, py = 20)
    set_path_f(path_frame)

    fenetre_frame = create_frame('Zoom', 0.5, 0.07, 0.15)
    set_fenetre_f(fenetre_frame)

    echelle_frame = create_frame('Echelles',0.67, 0.07, 0.3, 0.25)
    set_echelle_f(echelle_frame)


    param_frame = create_frame('Parametres à determiner', 0.67, 0.21, 0.3, 0.7)
    set_param_f(param_frame)
    
    analyser_b = tk.Button(text='valider', font=("Robot", 12), width= 20, height= 2,
                           command= get_res)
    analyser_b.place(relx=0.35, rely=0.18)

   
    root.mainloop()

main()