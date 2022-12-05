import diffchal_mono as dcmono
import diffchal_main as dcmain
import time
import numpy as np



def celsius_to_kelvin(T):
    return T + 273.15


start_time = time.time()


T0 = celsius_to_kelvin(20)
TS = 80

tmax = 360 # Temps finale en [ s ]
ymax = 0.1 # Longueur de la surface en y [ m ]
xmax = 0.1 # Longueur du fil / surface en x [ m ]

dt = 0.001
dy = 0.01
dx = 0.001


nt = int(tmax / dt)
nx = int(xmax / dx)

# Test = np.array([[[1, 2], [3, 4]], [[6, 7], [8, 9]]])
# print(Test[0, :, :])

cuivre = dcmain.Materiau("../datas/materials/cuivre.txt")
Fil_Cuivre = dcmono.Fil_homogene(0, xmax, cuivre)

src_centre = dcmono.Source_de_chaleur_mono(tmax, xmax, dt, dx)
ta = 1
tb = int(tmax/(2 * dt))
xa = int(xmax/(2 * dx))-1
xb = xa + 1
src_centre.ajouter_source(ta, tb, xa, xb, TS/(tb - ta))  # Temperature TS centre

Testbench = dcmono.Resolution_mono(tmax, xmax, dt, dx, T0)
Testbench.diffusion_chaleur_fil_homogene(Fil_Cuivre, src_centre)

print("Temperature maximale attendue :", T0 + TS)
print("Temperature maximale obtenue :", Testbench.Tmax)

Testbench.plot_crepe()

Testbench.terminer()
src_centre.terminer()

print(f"Programme executé en {'%.5s'%(time.time() - start_time)} secondes")