import gradio as gr
import scales as sc
from calculate_regions import analyse
from configs import detections
from scales import scales

def param_ckbox(region_name, region_list):
    with gr.Row():
        region_list[0] = gr.Checkbox(label= region_name)
        region_list[1] = gr.Textbox(label = "valeur minimale", value = region_list[1], interactive=True)
        region_list[2] = gr.Textbox(label = "valeur maximale", value = region_list[2], interactive=True)
        region_list[3] = gr.Textbox(label = "pourcentage de tolerance", value = region_list[3], interactive=True)
    return region_list

def analyse_ckbox(scale_name):
    value= False
    if scale_name == 'Kyte_Doolittle_scale':
        value = True
    return gr.Checkbox(label= scale_name, value = value)


def param_ckbox_list(scale):
    global detections
    if scale == 'AB': #change to antibody
        detections['r_Ac'] = []
    elif scale == "helice_a":  #change to antibody
        detections['r_helice'] = []


def detect():
    global detections
    for region in list(detections.keys()):
       detections[region] = param_ckbox(region, detections[region])

def analyse_tab():
   s_scale = []
   with gr.Row():
      with gr.Column():
        sequ_path = gr.Textbox(label = "nom du fichier pdb a analyser")
      with gr.Column():
        i = 0
        scales_name = list(scales.keys())
        while i < int(len(scales_name)/2):
            s_scale.append(analyse_ckbox(scales_name[i]).value)
            i += 1
      with gr.Column():
          while i < len(scales_name)/2:
            s_scale.append(analyse_ckbox(scales_name[i]).value)
            i += 1
   return sequ_path

def param_tab():
    with gr.Row():
        with gr.Column(scale = 2):
           gr.Markdown("### Detections")
           detect()
        with gr.Column(scale = 1):
            gr.Markdown("### Sequence analysee")
            start = gr.Textbox(label = "Numero d'AA du debut")
            stop = gr.Textbox(label = "Numero d'AA de la fin")
    return start, stop


global s_scale
with gr.Blocks(theme='finlaymacklon/smooth_slate') as demo:
    gr.Markdown("# Analyse de l'hydrophobicite des proteines")

    with gr.Tab("Analyse"):
        sequ_path = analyse_tab()
        s_scale = "Kyte_Doolittle_scale"

    with gr.Tab("Parametres"):
        debut, fin = param_tab()

    s_btn2 = gr.Button("Analyser")

    output = gr.Plot(label="Resultat")
    #s_btn2.click(analyse, inputs = [s_scale, sequ_path, debut, fin], outputs = [output])
    s_btn2.click(analyse, inputs = [sequ_path, debut, fin], outputs = [output])

demo.launch(server_name="0.0.0.0", share = True)
#demo.launch(share = True)