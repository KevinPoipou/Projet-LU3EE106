# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 09:18:05 2022

@author: 28732980
"""
import diffchal as diff 
    
Alumi = diff.Materiau(0,0,0) # initialisation de la dataclass

def get_datas(path): 
    
    d=diff.Materiau(0,0,0)
    with open (path,"r") as f: # lecture des fichiers txt
        lines =f.read().split ("\n")
        d.K=lines[0]
        d.C=lines[1]
        d.rho=lines[2]
    return d 
alumi=get_datas("./tab_alumi.txt") #valeurs de la dataclass du materiau alumi  
air =get_datas("./tab_air.txt") #valeurs  de la dataclass du materiau air  
cuivre=get_datas("./tab_cuivre.txt") # de la dataclass du materiau cuivre 
 


  