import diffchal_mono as dcmono
import diffchal_main as dcmain
import time



def celsius_to_kelvin(T):
    return T + 273.15


start_time = time.time()

xmax = 0.5 # Longueur du fil
tmax = 10 # Temps finale en [ s ]

dt = 0.001
dx = 0.01

nt = int(tmax / dt)
nx = int(xmax / dx)

cuivre = dcmain.Materiau("../datas/materials/cuivre.txt")
Fil_Cuivre = dcmono.Fil_homogene(0, xmax, cuivre)

f = dcmono.Source_de_chaleur_mono(tmax, xmax, dt, dx)
f.ajouter_source(1, 20, 25, 26, celsius_to_kelvin(90), celsius_to_kelvin(20))

Testbench = dcmono.Resolution_mono(tmax, xmax, dt, dx, celsius_to_kelvin(20))
Testbench.diffusion_chaleur_fil_homogene(Fil_Cuivre, f)
Testbench.plot_crepe()

Testbench.terminer()
f.terminer()

print(f"Programme executé en {'%.5s'%(time.time() - start_time)} secondes")