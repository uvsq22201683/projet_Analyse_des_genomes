import gradio as gr
import scales as sc

def ckbox(region_name, region_list):
    with gr.Row():
        region_list[0] = gr.Checkbox(label= region_name)
        region_list[1] = gr.Textbox(label = "valeur minimale", value = region_list[1])
        region_list[2] = gr.Textbox(label = "valeur maximale", value = region_list[2])
        region_list[3] = gr.Textbox(label = "pourcentage de tolerance", value = region_list[3])
    return region_list

detections = {'r_transmb': [True, 15, 25, 0], 
              'r_surface': [True, 3, 7, 0]} #move to config

def ckbox_list(scale):
    global detections
    if scale == 'AB': #change to antibody
        detections['r_Ac'] = []
    elif scale == "helice_a":  #change to antibody
        detections['r_helice'] = []


def detect():
    global detections
    for region in list(detections.keys()):
       detections[region] = ckbox(region, detections[region])

def analyse_tab():
   with gr.Column():
      with gr.Row():
        sequ_path = gr.Textbox(label = "nom du fichier pdb a analyser")
        scale = gr.Dropdown(choices = list(sc.scales.keys()), 
                                label = 'Choisissez le type de score')
      #s_bt1 = gr.Button("Appliquer")
      #s_bt1.click(ckbox_list, inputs = [scale])

def param_tab():
    with gr.Row():
        with gr.Column(scale = 2):
           gr.Markdown("### Detections")
           detect()
        with gr.Column(scale = 1):
            gr.Markdown("### Sequence analysee")
            start = gr.Textbox(label = "Numero d'AA du debut")
            stop = gr.Textbox(label = "Numero d'AA de la fin")



with gr.Blocks(theme='finlaymacklon/smooth_slate') as demo:
    gr.Markdown("# Analyse de l'hydrophobicite des proteines")

    with gr.Tab("Analyse"):
        analyse_tab()

    with gr.Tab("Parametres"):
        param_tab()

    s_btn2 = gr.Button("Analyser")

    output = gr.Plot(label="Resultat")
    #s_bt2.click(ckbox_list, inputs = [scale])

demo.launch(server_name="0.0.0.0", share = True)