from dataclasses import dataclass, field
import numpy as np
import os.path

"""
Fichier pour la resolution
"""

#%%

"""
Dataclass pour les materiaux
"""
@dataclass
class Materiau :
    """
    Classe specifique aux materiaux
    Initialise depuis le fichier '/datas/materials'
    Voir 'exemple.txt' pour ajouter un materiau
    """
    
    """
    Constantes
    """
    K : np.float64 = field(init=False)       # Conductivite thermique du materiau en [ W / (K * m) ]
    C : np.float64 = field(init=False)       # Capacite calorifique du materiau en [ J / (kg * K) ]
    rho : np.float64 = field(init=False)     # Masse volumique du materiau en [ kg / (m ^ 3) ]
    alfa : np.float64 = field(init=False)    # Diffusivite du materiau en [ m ^ 2 / s ]
    
    """
    Fonctions
    """
    def __init__(self, path: str):
        """
        Initialise les valeurs du materiau selon les valeurs stockees dans un fichier txt
        """
        if not(os.path.isfile(path)) :
            raise ValueError(f"Le fichier au lien {'%s'%path} n'existe pas.")
            
        fmat = open(path, 'r')          # Ouverture du fichier
        lgns = fmat.read().split('\n')  # Seperation en plusieurs lignes
        
        self.K = np.float64(lgns[0])    # Attribue la valeur de K du materiau
        self.C = np.float64(lgns[1])    # Attribue la valeur de C du materiau
        self.rho = np.float64(lgns[2])  # Attribue la valeur de rho du materiau
        
        fmat.close() # Fermeture du fichier
        
        self.alfa = self.K / (self.rho * self.C) # Calcul de la valeur de la diffusivite alfa du materiau

#%%

@dataclass
class Parametres_resolution :
    """
    Renseigne l'ensemble des paramètres
    """

    ## Init
    datamax : np.float64
    tmax : np.float64
    ymax : np.float64
    xmax : np.float64
    dt : np.float64
    dy : np.float64
    dx : np.float64
    T0 : np.float64
    
    res_mono : bool
    res_bi : bool
    
    ## Post Init
    dimt : int = field(init=False)
    dimy : int = field(init=False)
    dimx : int = field(init=False)
    
    dimmax_mono : int = field(init=False)
    dimmax_bi : int = field(init=False)
    
    exc_mono : bool = field(default=False, init=False) # Excessif en mono
    exc_bi : bool = field(default=False, init=False)   # Excessif en bi
    
    def __post_init__(self):
        self.dimt = int(self.tmax / self.dt)
        self.dimy = int(self.ymax / self.dy)
        self.dimx = int(self.xmax / self.dx)
        
        self.dimmax_mono = np.dtype(np.float64).itemsize * self.dimt * self.dimx
        self.dimmax_bi = np.dtype(np.float64).itemsize * self.dimt * self.dimy * self.dimx
        
        if self.dimmax_mono > self.datamax: self.exc_mono = True    
        if self.dimmax_bi > self.datamax: self.exc_bi = True


#%% PARTIE MONO-DIMENSIONNEL

@dataclass
class Matrice_temperature_mono :
    """
    """
    # Init
    Nom : str
    dimt : int
    dimx : int
    
    # Post Init
    Chemin_acces_mmap : str = field(init=False)
    M : np.memmap = field(init=False)     # Matrice des temperatures
    Tmin : np.float64 = field(init=False)
    Tmax : np.float64 = field(init=False)
    
    def __post_init__(self):
        self.Chemin_acces_mmap = '../datas/tmp/' + self.Nom 
        self.M = np.memmap(self.Chemin_acces_mmap, dtype=np.float64, mode='w+', shape=(self.dimt, self.dimx)) # Matrice des temperatures
        self.M[:, :] = 0
        self.Tmin = 0
        self.Tmax = 0    
    
    def __add__(self, other):
        self.M = self.M + other
        self.maj_T()
    
    def __sub__(self, other):
        self.M = self.M - other
        self.maj_T()
    
    def maj_T(self):
        """
        Mets à jour les temperatures min et max
        """
        self.Tmin = np.amin(self.M)
        self.Tmax = np.amax(self.M)    
        
    def ajouter_temp(self, ta: int, tb: int, xa: int, xb: int, T: np.float64) :
        """
        """
        self.M[ta:tb, xa:xb] = T
        self.maj_T()
    
    def terminer(self):
        """
        Supprime la memmap
        """
        #self.M._mmap.close()                              # Ferme la memmap
        del self.M                                       # Supprime l'objet
        os.remove(self.Chemin_acces_mmap)    # Supprime la memmap du systeme


#%%

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
    Composition : Materiau = field(init=False)  # Composition du fil
    
    """
    Fonction
    """
    def __init__(self, xa: np.float32, xb: np.float32, materiau: Materiau):
        self.xa = xa
        self.xb = xb
        self.longx = xb - xa
        self.Composition = materiau
        

#%%    

def diffusion_chaleur_fil_homogene(param_res: Parametres_resolution, fil: Fil_homogene, MSX: Matrice_temperature_mono):
    """
    Modélise la diffusion de la chaleur dans un fil homogene
    """

    MTX = Matrice_temperature_mono('Temperature_Res_Mono', param_res.dimt, param_res.dimx)      # Matrice Température avec composante X (mono-dimensionnel)
    MTX.ajouter_temp(0, param_res.dimt, 0, param_res.dimx, param_res.T0)                        # Ajout des températures initiales   

    print("Resolution mono-dimentionnel : Evaluation sur matrice de taille", MTX.M.shape)
    
    alfa = fil.Composition.alfa
    C2 = (alfa * param_res.dt) / (param_res.dx**2)
    C1 = (1 - (2 * (alfa * param_res.dt) / (param_res.dx**2)))

    for tau in range(1, param_res.dimt):

        TTX = MTX.M[tau-1, :]           # Tableau Temperature en X
        
        TTXP1 = MTX.M[tau-1, 1:]        # Tableau Temperature X+1
        TTXM1 = MTX.M[tau-1, :-1]       # Tableau Temperature X-1
        
        TTXP1 = np.hstack((TTXP1, 0))   # Ajout 0 en fin de TTXP1
        TTXM1 = np.hstack((0, TTXM1))   # Ajout 0 au début de TTXP1
    
        TSX = MSX.M[tau-1, :]        # Tableau temperature Source X
        
        MTX.M[tau, :] = (TTX * C1) + ((TTXP1 + TTXM1) * C2) + (TSX * param_res.dt)  # Calcul température à tau + 1
        
        # Conditions aux bords
        MTX.M[tau, 0] = MTX.M[tau-1, 0]     # Récupère la valeur précédante
        MTX.M[tau, -1] = MTX.M[tau-1, -1]   # Récupère la valeur précédante
    
         
    MTX.maj_T()
    
    return MTX

#%% PARTIE BI-DIMENTIONNEL

@dataclass
class Matrice_temperature_bi :
    """
    """
    # Init
    Nom : str
    dimt : int
    dimy : int
    dimx : int
    
    # Post Init
    Chemin_acces_mmap : str = field(init=False)
    M : np.memmap = field(init=False)     # Matrice des temperatures
    Tmin : np.float64 = field(init=False)
    Tmax : np.float64 = field(init=False)
    
    def __post_init__(self):
        self.Chemin_acces_mmap = '../datas/tmp/' + self.Nom 
        self.M = np.memmap(self.Chemin_acces_mmap, dtype=np.float64, mode='w+', shape=(self.dimt, self.dimy, self.dimx))  # Creer un tensor de dimension (dimt, dimy ,dimx)
        self.M[:, :, :] = 0
        self.Tmin = 0
        self.Tmax = 0    
    
    def __add__(self, other):
        self.M = self.M + other
        self.maj_T()
    
    def __sub__(self, other):
        self.M = self.M - other
        self.maj_T()
    
    def maj_T(self):
        """
        Mets à jour les temperatures min et max
        """
        self.Tmin = np.amin(self.M)
        self.Tmax = np.amax(self.M)     
        
    def ajouter_temp(self, ta: int, tb: int, ya: int, yb: int, xa: int, xb: int, T: np.float64) :
        """
        """
        self.M[ta:tb, ya:yb, xa:xb] = T
        self.maj_T()
    
    def terminer(self):
        """
        Supprime la memmap
        """
        #self.M._mmap.close()                              # Ferme la memmap
        del self.M                                       # Supprime l'objet
        os.remove(self.Chemin_acces_mmap)    # Supprime la memmap du systeme


#%%

@dataclass
class Surface_homogene :
    """
    Classe utile a la resolution de la diffusion de la chaleur en mono-dimensionnel
    """
    
    """
    Constantes
    """
    ya : np.float64             # Point de debut a en y 
    yb : np.float64             # Point de fin b en y 
    xa : np.float64             # Point de debut a en x 
    xb : np.float64             # Point de fin b en x 
    Composition : Materiau      # Composition de la surface
    #post init
    longy : np.float64 = field(init=False)          # Longueur de la surface en y
    longx : np.float64 = field(init=False)          # Longueur de la surface en x
    aire : np.float64 = field(init=False)
    
    
    """
    Fonction
    """
    def __post_init__(self):
        self.longy = self.yb - self.ya
        self.longx = self.xb - self.xa
        self.aire = self.longy * self.longx


#%%
    
def diffusion_chaleur_surface_homogene(param_res: Parametres_resolution, surf: Surface_homogene, MSYX: Matrice_temperature_bi):
    """
    Modélise la diffusion de la chaleur d'une surface homogène
    """

    MTYX = Matrice_temperature_bi('Temperature_Res_Mono', param_res.dimt, param_res.dimy, param_res.dimx)   # Matrice Température avec composante Y, X (bi-dimensionnel)
    MTYX.ajouter_temp(0, param_res.dimt, 0, param_res.dimy, 0, param_res.dimx, param_res.T0)                # Ajout des températures initiales

    print("Resolution bi-dim : Evaluation sur matrice de taille", MTYX.M.shape)
    
    alfa = surf.Composition.alfa
    C1 = (1 - 2 * alfa * param_res.dt * ((1/(param_res.dx**2)) + (1/(param_res.dy**2))))
    C2 = (alfa * param_res.dt)/(param_res.dx**2)
    C3 = (alfa * param_res.dt)/(param_res.dy**2)

    for tau in range(1, param_res.dimt):
        ZEROS_V = np.zeros((1, param_res.dimx)) # [0, 0, 0, 0, ...]
        ZEROS_H = np.zeros((param_res.dimy, 1)) # [[0], [0], [0], [0], ...]

        TTYX = MTYX.M[tau-1, :, :]              # Tableau Temperature en Y, X
        
        TTYP1 = MTYX.M[tau-1, 1:, :]            # Tableau Temperature Y+1
        TTYP1 = np.vstack((TTYP1, ZEROS_V))     # Ajout 0 en fin de TTYP1
        
        TTYM1 = MTYX.M[tau-1, :-1, :]           # Tableau Temperature Y-1
        TTYM1 = np.vstack((ZEROS_V, TTYM1))     # Ajout 0 au début de TTYM1
        
        TTXP1 = MTYX.M[tau-1, :, 1:]            # Tableau Temperature X+1
        TTXP1 = np.hstack((TTXP1, ZEROS_H))     # Ajout 0 en fin de TTXP1
        
        TTXM1 = MTYX.M[tau-1, :, :-1]           # Tableau Temperature X-1
        TTXM1 = np.hstack((ZEROS_H, TTXM1))     # Ajout 0 au début de TTXM1

        TSYX = MSYX.M[tau-1]                    # Tableau temperature Source Y, X
        
        MTYX.M[tau, :, :] = (TTYX * C1) + ((TTXP1 + TTXM1) * C2) + ((TTYP1 + TTYM1) * C3) + (TSYX * param_res.dt) # Calcul température à tau + 1
        
        # Condition aux bords
        MTYX.M[tau, 0, :] = MTYX.M[tau-1, 0, :]     # Récupère la valeur précédante
        MTYX.M[tau, -1, :] = MTYX.M[tau-1, -1, :]   # Récupère la valeur précédante
        MTYX.M[tau, :, 0] = MTYX.M[tau-1, :, 0]     # Récupère la valeur précédante
        MTYX.M[tau, :, -1] = MTYX.M[tau-1, :, -1]   # Récupère la valeur précédante
        
    MTYX.maj_T()
    
    return MTYX