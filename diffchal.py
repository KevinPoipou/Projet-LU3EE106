"""
Programme comprenant les fonctions utiles au projet
@version: 1.0
"""

from dataclasses import dataclass


"""
Dataclass pour les materiaux
"""
@dataclass
class materiau :
    """
    Constantes
    """
    K : float # Conductivite thermique [ W / (K * m) ]
    C : float # Capacite calorifique [ J / (kg * K) ]
    rho : float # Masse volumique [ kg / (m ^ 3) ]
    
    """
    Calcul et retourne la valeur de alfa
    @param1: self
    """
    def get_alfa(self) :
        return self.K / (self.rho * self.C)
