import configparser
import numpy as np
from plotManager import Parametres_figures
from diffchal import  Materiau, Parametres_resolution, Fil_homogene, Surface_homogene, Matrice_temperature_mono, Matrice_temperature_bi

config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = str

#%% PARAMETRES PAR DEFAUT

# Systeme
datamax = 200e6

# Constantes
tmax = 5
ymax = 0.1
xmax = 0.1
dt = 0.002
dy = 0.001
dx = 0.001
T0 = 20

# Resolution
resolution_mono = True
resolution_bi = True

# Materiau
fil = 'cuivre'
surface = 'cuivre'

# Source de chaleur
ta = 1
tb = int(tmax/(dt*2))
ya = int(ymax/(dy*2))-1
yb = int(ymax/(dy*2))
xa = int(xmax/(dx*2))-1
xb = int(xmax/(dx*2))
TA = 100

# Figures
autocolor = True
Tmin = 0
Tmax = 100
image_mono = True
graphique_mono = True
graphique_mono_point = int(xmax/(dx*2))-1
image_bi = True
image_bi_temps = int(tmax/(dt*2))
animation_mono = False
animation_bi = False


#%% DATACLASSE PARAMETRES


#%%

def etab_config():
    """
    Etablie le fichier config.ini
    """
    config['SYSTEME'] = {"# Section reservée aux paramères pour le systeme : \
                        \r#   - datamax : Taille maximum alloué aux memmaps [OCTETS]. \
                        \r# Attention cela correspond à la taille maximum attribué à une memmap et non à l'ensemble des memmaps" : None,
                         'datamax': datamax
                         }
        
    config['CONSTANTES'] = {"# Section reservée aux paramères généraux pour la résolution : \
                           \r#   - tmax : Temps maximum évalué [s]. \
                           \r#   - ymax : Longueur de l'axe y [m]. \
                           \r#   - xmax : Longueur de l'axe x [m]. \
                           \r#   - dt : Nombre de pas de temps [s]. \
                           \r#   - dy : Nombre de pas sur l'axe y [m]. \
                           \r#   - dx : Nombre de pas sur l'axe x [m]. \
                           \r#   - T0 : Temperature initiale [°C]." : None,
                            'tmax': tmax,
                            'ymax': ymax,
                            'xmax': xmax,
                            'dt': dt,
                            'dy': dy,
                            'dx': dx,
                            'T0': T0
                            }
    
    config['RESOLUTION'] = {"# Section reservée à la résolution et choix des méthodes utilisés: \
                           \r#   - resolution_monodimentionnel : Resolution de la diffusion de la chaleur dans un fil [True / False]. \
                           \r#   - resolution_bidimentionnel : Resolution de la diffusion de la chaleur dans une surface [True / False]. \
                           \r# La méthode des différence finies est utilisée pour la résolution" : None,
                            'resolution_mono': resolution_mono,
                            'resolution_bi': resolution_bi 
                            }
    
    config['MATERIAU'] = {"# Section reservée aux matériaux utilisés : \
                         \r#   - fil : Matériau composant le fil. \
                         \r#   - surface : Matériau composant la surface. \
                         \r# A noter que différents matériaux sont proposés par défaut : \
                         \r#   - cuivre \
                         \r#   - aluminium \
                         \r#   - air \
                         \r#   - debug (aucune diffusion) \
                         \r# Il est également possible d'ajouter de nouveaux matériaux. \
                         \r# Pour ce faire rendez-vous dans le fichier '/datas/materials' puis ajouter un fichier texte (format .txt) portant le nom du nouveau materiau. \
                         \r# Ouvrez ce fichier pour y spécifier les valeurs de la conductivité thermique, de la capacité calorifique et de la masse volumique du materiau. \
                         \r# Vous pouvez vous aider du fichier 'exemple.txt' pour voir comme rentrer ces valeurs correctement. \
                         \r# Une fois les valeurs rentrées, rentrer le nom du nouveau materiau (nom du fichier texte) dans les paramètres ci-dessous." : None,
                         'fil': fil,
                         'surface': surface
                         }
        
    config['SOURCE DE CHALEUR'] = {"# Section reservée aux paramères pour la résolution : \
                                  \r#   - ta : Temps de départ de la source [s / dt]. \
                                  \r#   - tb : Temps finale de la source [s / dt]. \
                                  \r#   - ya : Point de départ sur l'axe y [m / dy]. \
                                  \r#   - yb : Point d'arrivée sur l'axe y [m / dy]. \
                                  \r#   - xa : Point de départ sur l'axe x [m / dx]. \
                                  \r#   - xb : Point de départ sur l'axe x [m / dx]. \
                                  \r#   - TA : Temperature ajoutée au système [°C]. \
                                  \r# Avec :  \
                                  \r#   . 1 <= ta < tb <= (tmax-1)/dt Valeur entière \
                                  \r#   . 1 <= ya < yb <= (ymax-1)/dy Valeur entière \
                                  \r#   . 1 <= xa < xb <= (xmax-1)/dx Valeur entière \
                                  \r# Aussi ces valeurs peuvent influer sur la stabilité. \
                                  \r# Enfin ces paramètres peuvent prendre plusieurs entrées, séparé par une ','. \
                                  \r# Ainsi par exemple il est possible de rentrer les valeurs suivantes : \
                                  \r# ta = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 \
                                  \r# tb = 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250, 1250 \
                                  \r# ya = 29, 30, 31, 32, 32, 33, 33, 34, 34, 35, 35, 36, 40, 42, 43, 44, 44, 45, 45, 46, 46, 47, 47, 48, 48, 49, 49, 50, 50, 51, 51, 52, 52, 53, 53, 54, 55, 57, 57, 57, 57, 57, 60, 61, 61, 62, 63, 63, 64, 64, 65, 65, 65, 66, 66, 67, 67, 68 \
                                  \r# yb = 30, 31, 32, 33, 33, 34, 34, 35, 35, 36, 36, 40, 42, 43, 44, 45, 45, 46, 46, 47, 47, 48, 48, 49, 49, 50, 50, 51, 51, 52, 52, 53, 53, 54, 54, 55, 57, 61, 61, 61, 61, 60, 61, 62, 63, 63, 64, 64, 65, 65, 66, 66, 66, 67, 67, 68, 68, 69 \
                                  \r# xa = 46, 43, 41, 39, 49, 39, 52, 38, 53, 38, 54, 55, 54, 53, 51, 48, 60, 45, 59, 43, 58, 41, 56, 40, 54, 39, 51, 38, 47, 38, 44, 38, 42, 37, 41, 40, 39, 38, 55, 46, 49, 51, 51, 38, 54, 39, 39, 53, 40, 51, 41, 49, 51, 42, 51, 43, 50, 46 \
                                  \r# xb = 51, 55, 56, 45, 57, 41, 58, 40, 59, 39, 59, 59, 59, 58, 57, 56, 61, 55, 60, 53, 60, 51, 59, 47, 58, 44, 57, 41, 56, 39, 54, 39, 52, 38, 48, 45, 43, 42, 59, 47, 50, 53, 52, 43, 58, 43, 44, 58, 46, 57, 46, 50, 56, 47, 55, 48, 54, 51 \
                                  \r# TA = 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100 \
                                  \r# Cela correspond à appliquer une source de chaleur avec la forme du logo de Sorbonne Université (visible en bidimentionnel).": None,
                                    'ta': ta,
                                    'tb': tb,
                                    'ya': ya,
                                    'yb': yb,
                                    'xa': xa,
                                    'xb': xb,
                                    'TA': TA
                                    }
     
    config['FIGURES'] = {"# Section reservé aux paramères pour l'affichage : \
                        \r#   - autocolor : Echelonnage automatique des couleurs pour les images [True / False]. \
                        \r#   - Tmin : Temperature minimal de l'echelle de temperature (appliquée si autocolor = False) [°C]. \
                        \r#   - Tmax : Temperature maximal de l'echelle de temperature (appliquée si autocolor = False) [°C]. \
                        \r#   - image_mono : Créer une figure permettant d'observer la diffusion de la chaleur dans un fil en tout point en tout temps [True / False]. \
                        \r#   - graphique_mono : Créer un graphique permettant d'observer la diffusion de la chaleur dans un fil en un point spécifié par 'graphique_mono_point' en tout temps [True / False]. \
                        \r#   - graphique_mono_point : Point observé avec le graphique 'graphique_monodimentionnel [m / dx]' \
                        \r#   - image_bi : Créer une figure permettant d'observer la diffusion de la chaleur dans une surface en tout point à un temps spécifié par 'image_bi_temps' [True / False]. \
                        \r#   - animation_mono : Créer une animation representant la diffusion de la chaleur dans un fil [True / False] \
                        \r#   - animation_bi : Créer une animation representant la diffusion de la chaleur dans une surface [True / False] \
                        \r# À noter que les animations peuvent mettre un certain temps à être créée." : None,
                          'autocolor': autocolor,
                          'Tmin': Tmin,
                          'Tmax': Tmax,
                          'image_mono': image_mono,
                          'graphique_mono': graphique_mono,
                          'graphique_mono_point': graphique_mono_point,
                          'image_bi': image_bi,
                          'image_bi_temps': image_bi_temps,
                          'animation_mono': animation_mono,
                          'animation_bi': animation_bi
                          }
        
    with open('../config.ini', 'w') as configfile:
      config.write(configfile)

    
#%% RECUPERATION PARAMETRES

def lire_config_parametres():
    config.read('../config.ini')
    
    ldatamax = np.float64(config.get('SYSTEME', 'datamax', fallback=datamax))
    ltmax = np.float64(config.get('CONSTANTES', 'tmax', fallback=tmax))
    lymax = np.float64(config.get('CONSTANTES', 'ymax', fallback=ymax))
    lxmax = np.float64(config.get('CONSTANTES', 'xmax', fallback=xmax))
    ldt = np.float64(config.get('CONSTANTES', 'dt', fallback=dt))
    ldy = np.float64(config.get('CONSTANTES', 'dy', fallback=dy))
    ldx = np.float64(config.get('CONSTANTES', 'dx', fallback=dx))
    lT0 = np.float64(config.get('CONSTANTES', 'T0', fallback=T0))
    lres_mono = config.getboolean('RESOLUTION', 'resolution_mono', fallback=resolution_mono)
    lres_bi = config.getboolean('RESOLUTION', 'resolution_bi', fallback=resolution_bi)
    lautocolor = config.getboolean('FIGURES', 'autocolor', fallback=autocolor)
    lvmin = np.float64(config.get('FIGURES', 'vmin', fallback=Tmin))
    lvmax = np.float64(config.get('FIGURES', 'vmax', fallback=Tmax))
    limage_mono = config.getboolean('FIGURES', 'image_mono', fallback=image_mono)
    lgraphique_mono = config.getboolean('FIGURES', 'graphique_mono', fallback=graphique_mono)
    lgraphique_mono_point = config.getint('FIGURES', 'graphique_mono_point', fallback=graphique_mono_point)
    limage_bi = config.getboolean('FIGURES', 'image_bi', fallback=image_bi)
    
    limage_bi_temps = config.getint('FIGURES', 'image_bi_temps', fallback=image_bi_temps)
    
    lanimation_mono = config.getboolean('FIGURES', 'animation_mono', fallback=animation_mono)
    lanimation_bi = config.getboolean('FIGURES', 'animation_bi', fallback=animation_bi)
    
    lT0 += 273.15 # Conversion en °K
    
    param_res = Parametres_resolution(ldatamax, ltmax, lymax, lxmax, ldt, ldy, ldx, lT0, lres_mono, lres_bi)
    
    if param_res.exc_mono == True and param_res.res_mono == True:
        raise ValueError(f"La taille des memmaps créées lors de la résolutions en mono-dimensionnel excèdent la taille maximum autorisé de {'%d'%(param_res.dimmax_mono - param_res.datamax)} octets.\
                         \nPour remedier à ce problème, vous pouvez dans le fichier 'config.ini' : \
                         \n - Augmenter la valeur de 'datamax', \
                         \n - Réduire les paramètres 'tmax' et/ou 'xmax', \
                         \n - Augmenter les valeurs de 'dt' et/ou 'dx'.")
    
    if param_res.exc_bi == True and param_res.res_bi == True:
        raise ValueError(f"La taille des memmaps créées lors de la résolutions en bi-dimensionnel excèdent la taille maximum autorisé de {'%d'%(param_res.dimmax_bi - param_res.datamax)} octets.\
                         \nPour remedier à ce problème, vous pouvez dans le fichier 'config.ini' : \
                         \n - Augmenter la valeur de 'datamax', \
                         \n - Réduire les paramètres 'tmax' et/ou 'ymax' et/ou 'xmax', \
                         \n - Augmenter les valeurs de 'dt' et/ou 'dy' et/ou 'dx'.")

    param_fig = Parametres_figures(lautocolor, lvmin, lvmax, limage_mono, lgraphique_mono, lgraphique_mono_point, limage_bi, limage_bi_temps, lanimation_mono, lanimation_bi)                    
    
    return param_res, param_fig


#%% PARTIE MONO-DIMENSIONNEL

def lire_config_fil_homogene(param_res: Parametres_resolution):
    config.read('../config.ini')
    materiau_config = config.get('MATERIAU', 'fil', fallback='cuivre')
    
    if materiau_config == 'exemple' :
        raise ValueError("Le materiau 'exemple' ne peut pas être utilisé.\
                        \nPour remedier à ce problème, vous pouvez changer le materiau spécifié au paramètre 'fil' dans la section 'MATERIAU' dans le fichier 'config.ini'")
    
    lien_vers_materiau = "../datas/materials/" + materiau_config +".txt"
    
    materiau_fil = Materiau(lien_vers_materiau)
    
    fil = Fil_homogene(0, param_res.xmax, materiau_fil)
    
    return fil


def lire_config_src_chaleur_mono(param_res: Parametres_resolution):
    config.read('../config.ini')

    lta = config.get('SOURCE DE CHALEUR', 'ta', fallback=str(ta)).split(",")
    ltb = config.get('SOURCE DE CHALEUR', 'tb', fallback=str(tb)).split(",")
    lxa = config.get('SOURCE DE CHALEUR', 'xa', fallback=str(xa)).split(",")  
    lxb = config.get('SOURCE DE CHALEUR', 'xb', fallback=str(xb)).split(",")
    lTA = config.get('SOURCE DE CHALEUR', 'TA', fallback=str(TA)).split(",")
    
    lta = list(map(int, lta))
    ltb = list(map(int, ltb))
    lxa = list(map(int, lxa))
    lxb = list(map(int, lxb))
    lTA = list(map(int, lTA))
    
    comp = [lta, ltb, lxa, lxb]
    
    if not all(len(l) == len(lTA) for l in comp):
        raise ValueError("Toutes les listes ne font pas la même taille.\
                        \nIl est nécessaire que tous les paramètres (ta, tb, xa, ...) est le même nombre d'éléments dans la section 'SOURCE DE CHALEUR' de 'config.ini'.")

    src_chaleur_mono = Matrice_temperature_mono('Source_chaleur_mono', param_res.dimt, param_res.dimx)

    for i in range(len(lTA)):
        print(f"Source de chaleur de {'%d'%lTA[i]}°C ajoutée à ta : {'%d'%lta[i]}, tb : {'%d'%ltb[i]}, xa : {'%d'%lxa[i]}, xb : {'%d'%lxb[i]}")
        src_chaleur_mono.ajouter_temp(lta[i], ltb[i], lxa[i], lxb[i], lTA[i])
    
    return src_chaleur_mono

    
#%% PARTIE BI-DIMENSIONNEL

def lire_config_surface_homogene(param_res: Parametres_resolution):
    config.read('../config.ini')
    materiau_config = config.get('MATERIAU', 'surface', fallback='cuivre')
    
    if materiau_config == 'exemple' :
        raise ValueError("Le materiau 'exemple' ne peut pas être utilisé.\
                        \nPour remedier à ce problème, vous pouvez changer le materiau spécifié au paramètre 'surface' dans la section 'MATERIAU' dans le fichier 'config.ini'")
    
    lien_vers_materiau = "../datas/materials/" + materiau_config +".txt"
    
    materiau_surface = Materiau(lien_vers_materiau)
    
    fil = Surface_homogene(0, param_res.ymax, 0, param_res.xmax, materiau_surface)
    
    return fil
    

def lire_config_src_chaleur_bi(param_res: Parametres_resolution):
    config.read('../config.ini')

    lta = config.get('SOURCE DE CHALEUR', 'ta', fallback=str(ta)).split(",")
    ltb = config.get('SOURCE DE CHALEUR', 'tb', fallback=str(tb)).split(",")
    lya = config.get('SOURCE DE CHALEUR', 'ya', fallback=str(ya)).split(",")
    lyb = config.get('SOURCE DE CHALEUR', 'yb', fallback=str(yb)).split(",")
    lxa = config.get('SOURCE DE CHALEUR', 'xa', fallback=str(xa)).split(",")
    lxb = config.get('SOURCE DE CHALEUR', 'xb', fallback=str(xb)).split(",")
    lTA = config.get('SOURCE DE CHALEUR', 'TA', fallback=str(TA)).split(",")
    
    lta = list(map(int, lta))
    ltb = list(map(int, ltb))
    lya = list(map(int, lya))
    lyb = list(map(int, lyb))
    lxa = list(map(int, lxa))
    lxb = list(map(int, lxb))
    lTA = list(map(int, lTA))
    
    comp = [lta, ltb, lya, lyb, lxa, lxb]
    
    if not all(len(l) == len(lTA) for l in comp):
        raise ValueError("Toutes les listes ne font pas la même taille.\
                        \nIl est nécessaire que tous les paramètres (ta, tb, xa, ...) est le même nombre d'éléments dans la section 'SOURCE DE CHALEUR' de 'config.ini'.")

    src_chaleur_bi = Matrice_temperature_bi('Source_chaleur_bi', param_res.dimt, param_res.dimy, param_res.dimx)
    for i in range(0, len(lTA)):
        print(f"Source de chaleur de {'%d'%lTA[i]}°C ajoutée à ta : {'%d'%lta[i]}, tb : {'%d'%ltb[i]}, ya : {'%d'%lya[i]}, yb : {'%d'%lyb[i]}, xa : {'%d'%lxa[i]}, xb : {'%d'%lxb[i]}")
        src_chaleur_bi.ajouter_temp(lta[i], ltb[i], lya[i], lyb[i], lxa[i], lxb[i], lTA[i])
    
    return src_chaleur_bi