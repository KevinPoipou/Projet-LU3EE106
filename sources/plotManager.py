import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
import numpy as np
from diffchal import Matrice_temperature_mono, Matrice_temperature_bi, Parametres_resolution


#%% Configurations des textes des figures

plt.rcParams.update({
    "font.weight": "bold",
    "xtick.major.pad": 7,
    "xtick.labelsize": 16,
    "ytick.major.pad": 7,
    "ytick.labelsize": 16,
    "figure.titlesize" : 24,
    "figure.titleweight" : "bold",
    "axes.labelsize" : 16,
    "axes.labelweight" : "semibold",
    "figure.figsize" : (8,8)
})


#%% Dataclass pour les paramètres des figures

@dataclass
class Parametres_figures :
    """
    Renseigne l'ensemble des paramètres pour la création des figures
    """
    autocolor : bool
    Tmin : np.float64
    Tmax : np.float64
    image_mono : bool
    graph_mono : bool
    graph_mono_point : int
    image_bi : True
    image_bi_temps : int
    animation_mono : bool
    animation_bi : bool


#%% PARTIE MONO-DIMENSIONNEL

def image_mono(Mat_mono: Matrice_temperature_mono, param_res: Parametres_resolution, param_fig: Parametres_figures) :
    """
    Affiche la matrice des temperatures retournee -- Resulte un empilement des fils
    """
    
    vmin = Mat_mono.Tmin
    vmax = Mat_mono.Tmax

    if param_fig.autocolor == False:
        vmin = param_fig.Tmin
        vmax = param_fig.Tmax
    
    graph_titre = "Diffusion de la chaleur en tout point d'un fil"
    path = '../exports/figures/' + graph_titre + '.png'
    cmap = plt.get_cmap('jet')
    fig, ax = plt.subplots()

    im = ax.imshow(Mat_mono.M, cmap=cmap, vmin=vmin, vmax=vmax, aspect='auto', origin='lower')
    
    label_y = np.linspace(0, Mat_mono.dimt, 11)
    ax.set_yticks(label_y, ['%.1f' %val for val in label_y * param_res.dt])
    
    ax.set_xlim(0, Mat_mono.dimx-1)
    ax.autoscale(enable = 'true',axis = 'both')
    
    fig.suptitle(graph_titre)
    ax.set_ylabel('Temps [s]')
    ax.set_xlabel('Longueur du fil [mm]')
    
    plt.colorbar(im, ax=ax, label = 'Temperature [°C]', ticks=np.linspace(vmin, vmax, 10), format='%.2f') #Affiche une bar de couleur
    fig.set_figheight(16)
    fig.set_figwidth(16)
    fig.savefig(path, dpi=300, bbox_inches = "tight")
    print('Image créée à', path)
    
    plt.show()


def graphique_mono(Mat_mono: Matrice_temperature_mono, param_fig: Parametres_figures) :
    x = param_fig.graph_mono_point
    centre = Mat_mono.M[:,x]
    centreDegres = centre
    t = np.linspace(0,Mat_mono.dimt,np.shape(centre)[0])
    plt.plot(t/1000,centreDegres)
    plt.suptitle("Evolution de la temperature en un point du fil")
    plt.ylabel('Temperature [°C]')
    plt.xlabel('Temps [s]')
    
    graph_titre = 'Evolution de la temperature'
    path = '../exports/figures/' + graph_titre + '.png'

    plt.savefig(path, dpi=300, bbox_inches = "tight")
    print('Image créée à', path)
    plt.show()


def animation_mono(Mat_mono: Matrice_temperature_mono, param_fig: Parametres_figures) :
    """
    Creer et enregistre une animation
    """
    
    fig, ax = plt.subplots()

    vmin = Mat_mono.Tmin
    vmax = Mat_mono.Tmax

    if param_fig.autocolor == False:
        vmin = param_fig.Tmin
        vmax = param_fig.Tmax

    ims = []
    cmap = plt.get_cmap('jet')
    for i in range(0, Mat_mono.dimt-1):
        M = Mat_mono.M[i, :].reshape((Mat_mono.dimx, 1))
        im = ax.imshow(M, animated=True, cmap=cmap, vmin=vmin, vmax=vmax, origin='lower')        
        ims.append([im])
    
    print("Création de l'animation.\nCela peut prendre du temps.")
    ani = animation.ArtistAnimation(fig, ims, interval=0.1, blit=True, repeat_delay=1000)
    
    ani_titre = 'Diffusion de la chaleur dans un fil'
    path = '../exports/animations/' + ani_titre + '.gif'
    ani.save(path, dpi=150)
    print('Animation créée à', path)


#%% PARTIE BI-DIMENSIONNEL

def image_surface(Mat_bi: Matrice_temperature_bi, param_fig: Parametres_figures) :
    """
    """
    
    vmin = Mat_bi.Tmin
    vmax = Mat_bi.Tmax

    if param_fig.autocolor == False:
        vmin = param_fig.Tmin
        vmax = param_fig.Tmax
    
    graph_titre = 'Diffusion de la chaleur dans une surface'
    path = '../exports/figures/' + graph_titre + '.png'
    cmap = plt.get_cmap('jet')
    
    fig, ax = plt.subplots()

    im = ax.imshow(Mat_bi.M[param_fig.image_bi_temps, :, :], cmap=cmap, vmin=vmin, vmax=vmax, aspect='auto', origin='lower')
    
    fig.suptitle(graph_titre)
    ax.set_ylabel('Hauteur de la surface [mm]')
    ax.set_xlabel('Longueur de la surface [mm]')
    plt.colorbar(im, ax=ax, label = 'Temperature [°C]', ticks=np.linspace(vmin, vmax, 10), format='%.2f') #Affiche une bar de couleur

    fig.set_figheight(16)
    fig.set_figwidth(16)
    fig.savefig(path, dpi=300, bbox_inches = "tight")
    print('Image créée à', path)
    
    plt.show()


def animation_bi(Mat_bi: Matrice_temperature_bi, param_fig: Parametres_figures) :
    """
    Creer et enregistre une animation
    """
    
    vmin = Mat_bi.Tmin
    vmax = Mat_bi.Tmax

    if param_fig.autocolor == False:
        vmin = param_fig.Tmin
        vmax = param_fig.Tmax
    
    fig, ax = plt.subplots()

    ims = []
    cmap = plt.get_cmap('jet')
    for i in range(0, Mat_bi.dimt-1):
        im = ax.imshow(Mat_bi.M[i, :, :], animated=True, cmap=cmap, vmin=vmin, vmax=vmax, origin='lower')
        t = ax.annotate(i,(1,1))
        ax.set_ylabel('Hauteur de la surface [mm]')
        ax.set_xlabel('Longueur de la surface [mm]')
        ims.append([im, t])
    
    print("Création de l'animation.\nCela peut prendre du temps.")
    ani = animation.ArtistAnimation(fig, ims, interval=0.1, blit=True, repeat_delay=1000)
    
    ani_titre = 'Diffusion de la chaleur dans une surface'
    path = '../exports/animations/' + ani_titre + '.gif'
    ani.save(path, dpi=150)
    print('Animation créée à', path)