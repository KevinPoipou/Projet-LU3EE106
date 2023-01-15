import diffchal
import configManager as conf
import plotManager as plm
import time
import os.path


#%% MESSAGE PREVENTIF

print("Il est recommandé d'executer ce programme sur une machine dont l'utilisateur est administrateur")


#%% CREATIONS DES FICHIERS ET DOSSIER NECESSAIRES A L'EXECUTIONS

if not os.path.exists('../exports'):
    os.makedirs('../exports')

if not os.path.exists('../exports/figures'):
    os.makedirs('../exports/figures')

if not os.path.exists('../exports/animations'):
    os.makedirs('../exports/animations')

if not os.path.exists('../datas/tmp'):
    os.makedirs('../datas/tmp')

if not(os.path.isfile('../config.ini')) :
    """
    Si le fichier config.ini n'existe pas, le creer.
    """
    conf.etab_config()

Param_res, Param_fig = conf.lire_config_parametres()


#%% DEBUT CHRONOMETRAGE

start_time = time.time()


#%% RESOLUTION DIFFUSION DE LA CHALEUR EN MONO-DIMENSIONNEL (FIL HOMOGENE)

if Param_res.res_mono == True :        

    Fil = conf.lire_config_fil_homogene(Param_res) # Recuperations des données depuis le fichier config.ini

    Src_chaleur_mono = conf.lire_config_src_chaleur_mono(Param_res) # Recuperations des données depuis le fichier config.ini

    Model_mono = diffchal.diffusion_chaleur_fil_homogene(Param_res, Fil, Src_chaleur_mono)  # Modelisation de la diffusion de chaleur dans un fil

    Model_mono - 273.15   # Conversion en °C

    if Param_fig.image_mono == True : plm.image_mono(Model_mono, Param_res, Param_fig)  # Creation image
    if Param_fig.graph_mono == True : plm.graphique_mono(Model_mono, Param_fig)         # Creation graphique
    if Param_fig.animation_mono == True : plm.animation_mono(Model_mono, Param_fig)     # Creation animation

    Src_chaleur_mono.terminer() # Suppression des memmaps
    Model_mono.terminer()       # Suppression des memmaps


#%% RESOLUTION DIFFUSION DE LA CHALEUR EN BI-DIMENSIONNEL (SURFACE HOMOGENE)
    
if Param_res.res_bi == True :
    
    Surface = conf.lire_config_surface_homogene(Param_res) # Recuperations des données depuis le fichier config.ini
    
    Src_chaleur_bi = conf.lire_config_src_chaleur_bi(Param_res) # Recuperations des données depuis le fichier config.ini

    Model_bi = diffchal.diffusion_chaleur_surface_homogene(Param_res, Surface, Src_chaleur_bi) # Modelisation de la diffusion de chaleur dans une surface

    Model_bi - 273.15   # Conversion en °C

    if Param_fig.image_bi == True : plm.image_surface(Model_bi, Param_fig)  # Creation image
    if Param_fig.animation_bi == True : plm.animation_bi(Model_bi, Param_fig) # Creation animation

    Model_bi.terminer() # Suppression des memmaps
    Src_chaleur_bi.terminer() # Suppression des memmaps


#%% FIN CHRONOMETRAGE

print(f"Programme executé en {'%.5s'%(time.time() - start_time)} secondes")