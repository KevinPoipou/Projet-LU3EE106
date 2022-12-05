from dataclasses import dataclass, field
import matplotlib.pyplot as plt
import diffchal_main as dcm
import numpy as np
import os

"""
Fichier contenant l'ensemble des fonctions et classes utilent a la resolution diffusion de la chaleur en mono-dimensionnelle
"""

@dataclass
class Source_de_chaleur_mono :
    """
    Classe specifique au source de chaleur (note r)
    A utiliser pour la resolution en mono-dim
    """
    
    """
    Constantes
    """
    dimt : int = field(init=False)
    dimx : int = field(init=False)
    M_T : np.memmap = field(init=False) # Matrice des Temperatures
    
    """
    Fonctions
    """
    def __init__(self, tmax: np.float32, xmax: np.float32, dt: np.float64, dx: np.float64):
        """
        """
        self.dimt = int(tmax / dt)
        self.dimx = int(xmax / dx)
        self.M_T = np.memmap('../datas/tmp/Source_de_chaleur_mono', dtype=np.float64, mode='w+', shape=(self.dimt, self.dimx))  # Creer une matrice de dimension (dimt, dimx) de valeur 0
    
    def ajouter_source(self, ta: int, tb: int, xa: int, xb: int, T: np.float64) :
        """
        """
        self.M_T[ta:tb, xa:xb] = T
        
    def terminer(self):
        """
        Supprime la memmap
        """
        self.M_T._mmap.close()                              # Ferme la memmap
        del self.M_T                                        # Supprime l'objet
        os.remove('../datas/tmp/Source_de_chaleur_mono')    # Supprime la memmap du systeme


@dataclass
class Fil_homogene :
    """
    Classe utile a la resolution de la diffusion de la chaleur en mono-dimensionnel
    """
    
    """
    Constantes
    """
    xa : np.float64 = field(init=False)             # Point de debut a en x 
    xb : np.float64 = field(init=False)             # Point de fin b en x 
    longx : np.float64 = field(init=False)          # Longueur du fil en x
    Composition : dcm.Materiau = field(init=False)  # Composition du fil
    
    """
    Fonction
    """
    def __init__(self, xa: np.float32, xb: np.float32, materiau: dcm.Materiau):
        self.xa = xa
        self.xb = xb
        self.longx = xb - xa
        self.Composition = materiau


@dataclass
class Resolution_mono :
    """
    """
    
    """
    Constantes
    """
    ## Init
    tmax : np.float64
    xmax : np.float64
    dt : np.float64
    dx : np.float64
    T0 : np.float64
    ## Post Init
    dimt : int = field(init=False)
    dimx : int = field(init=False)
    M_T : np.memmap = field(init=False)    # Matrice des temperatures
    Tmin : np.float64 = field(init=False)
    Tmax : np.float64 = field(init=False)
    
    """
    Fonctions
    """
    def __post_init__(self):
        self.dimt = int(self.tmax / self.dt)
        self.dimx = int(self.xmax / self.dx)
        self.M_T = np.memmap('../datas/tmp/Diffusion_chaleur_mono', dtype=np.float64, mode='w+', shape=(self.dimt, self.dimx)) # Matrice des temperatures
        self.M_T[:, :] = self.T0
        self.Tmin = self.T0
        self.Tmax = self.T0
        
    
    def diffusion_chaleur_fil_homogene(self, fil : Fil_homogene, f: Source_de_chaleur_mono):
        """
        @param1 : self
        @param2 : fil, renseigne les constantes d'un fil homogene
        @param3 : r, matrice des sources de chaleurs
        
        Matrice des temperatures :
                x0      x1      x2      x3      ...
        t0      T00     T10     T20     T30
        t1      T01     T11     T21     T31
        t2      T02     T12     T22     T32
        ...
        
        Cette matrice est stockée dans une memmap M_T
        """

        print("Resolution mono-dim : Evaluation sur matrice de taille", self.M_T.shape)
        
        alfa = fil.Composition.alfa
        c = (alfa * self.dt) / (self.dx**2) # Constantes
        
        c1 = (self.dt + (self.dx/2))
        c2 = (alfa/2)

        for t in range(0, self.dimt-1, 1):  #t
        
            if(t == int(self.dimt/4)-1) :
                print('25%')
            if(t == int(self.dimt/2)-1) :
                print('50%')
            if(t == int(3*self.dimt/4)-1) :
                print('75%')
            if(t == self.dimt-2) :
                print('100%')
            
            self.M_T[t+1, 0] = self.M_T[t, 1]
            self.M_T[t+1, -1] = self.M_T[t, -2]

            for x in range(1, self.dimx-1, 1): #x
            
                # self.M_T[t+1, x] = c1 * f.M_T[t, x] + c2 * (self.M_T[t, x-1] + self.M_T[t, x+1])
             
                TP = self.M_T[t, x] * (1 - (2 * c))             # Temperature au point en x au temps t
                TV = (self.M_T[t, x+1] + self.M_T[t, x-1]) * c  # Temperature aux voisinages du point en x au temps t
                F = f.M_T[t, x] * self.dt     # Fonction f(x, t) au point en x au temps t
    
                # if(F == self.M_T[t, x]):
                #     F = 0;
    
                self.M_T[t+1, x] = TP + TV + F                  # Temperature au point en x au temps t+1
            
            
        self.Tmin = np.amin(self.M_T)
        self.Tmax = np.amax(self.M_T)


    def plot_crepe(self) :
        """
        Retourne la matrice des temperatures (comme une crepe) et l'affiche -- Resulte un empilement des fils
        """
        graph_titre = 'Diffusion de la chaleur dans un fil mis en pile'
        path = '../exports/figures/' + graph_titre + '.png'
        cmap = plt.get_cmap('jet')
        
        fig, ax = plt.subplots()

        im = ax.imshow(self.M_T, cmap=cmap, vmin=self.Tmin, vmax=self.Tmax, aspect='auto')
        ax.invert_yaxis()
        
        label_x = np.arange(0, self.dimx, (2*self.dimx)/(self.dimx*self.dx))
        label_y = np.arange(0, self.dimt, (2*self.dimt)/(self.dimt*self.dx))
        
        ax.set_xticks(label_x, ['%d' %val for val in label_x * self.dx])
        ax.set_yticks(label_y, ['%.1f' %val for val in label_y * self.dt])
        
        ax.set(title=graph_titre, xlabel='x', ylabel='Temps')
        plt.colorbar(im, ax=ax, label = 'Temperature', ticks=np.linspace(self.Tmin, self.Tmax, 10), format='%.2f') #Affiche une bar de couleur

        fig.set_figheight(10)
        fig.set_figwidth(16)
        fig.savefig(path, dpi=300, bbox_inches = "tight")
        print('Image créée à', path)
        
        plt.show()
    
    def terminer(self):
        """
        Supprime la memmap
        """
        self.M_T._mmap.close()                              # Ferme la memmap
        del self.M_T                                        # Supprime l'objet
        os.remove('../datas/tmp/Diffusion_chaleur_mono')    # Supprime la memmap du systeme