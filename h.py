import tkinter as tk
import configs
from configs import colors

root = tk.Tk()
root.title('Analyse de genome')
largeur_ecran = root.winfo_screenwidth()
hauteur_ecran = root.winfo_screenheight()
root.geometry(f"{largeur_ecran}x{hauteur_ecran}")
root.configure(bg = 'white')
root.resizable(False,False)



def coul():
    colors_list = "\n".join([f"{key} : {value}" for key, value in colors.items()])
    return colors_list

legend_text = coul()  # Appel de la fonction pour obtenir la liste des couleurs
legend_label = tk.Label(root, text=legend_text, font=("Courier New", 10))
legend_label.place(relx=0.5, rely=0.6)



root.mainloop()

         
