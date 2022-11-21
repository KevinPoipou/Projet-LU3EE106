# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 08:47:36 2022

@author: Poipou
"""

import numpy as np
from matplotlib import pyplot as plt
from dataclasses import dataclass

@dataclass
class test :
    x : np.array
    y : float
    t : np.array
    

a1 = test([1,2,5,10],1,[0,100,10,1000])
a2 = test([1,2,5,10],2,[0,10,120,100])


plt.figure()
plt.tight_layout()
plt.suptitle("Titre")
plt.xlabel("x")
plt.ylabel("Temps")
plt.ylim(-1,10)
#for i in range(len(test.x)) :
plt.scatter(a1.x, np.full(len(a1.x),a1.y), c=a1.t, cmap='jet')
plt.scatter(a2.x, np.full(len(a2.x),a2.y), c=a2.t, cmap='jet')
plt.colorbar(label = "Temperature")
