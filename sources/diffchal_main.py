from dataclasses import dataclass, field
import numpy as np

"""
Fichier pour la resolution
"""


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
        fmat = open(path, 'r')          # Ouverture du fichier
        lgns = fmat.read().split('\n')  # Seperation en plusieurs lignes
        
        self.K = np.float64(lgns[0])    # Attribue la valeur de K du materiau
        self.C = np.float64(lgns[1])    # Attribue la valeur de C du materiau
        self.rho = np.float64(lgns[2])  # Attribue la valeur de rho du materiau
        
        fmat.close() # Fermeture du fichier
        
        self.alfa = self.K / (self.rho * self.C) # Calcul de la valeur de la diffusivite alfa du materiau