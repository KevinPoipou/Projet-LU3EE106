import diffchal_mono as dcmono
import diffchal_main as dcmain
import time



def celsius_to_kelvin(T):
    return T + 273.15


start_time = time.time()



xmax = 10 # Longueur du fil
tmax = 10 # Temps finale en [ s ]

dt = 0.001
dx = 0.01



nt = int(tmax / dt)
nx = int(xmax / dx)



cuivre = dcmain.Materiau("../datas/materials/cuivre.txt")
Fil_Cuivre = dcmono.Fil_homogene(0, xmax, cuivre)

r = dcmono.Source_de_chaleur_mono(tmax, xmax, dt, dx)
r.ajouter_source(1, 3000, 495, 505, celsius_to_kelvin(90))

Testbench = dcmono.Resolution_mono(tmax, xmax, dt, dx, celsius_to_kelvin(20))
Testbench.diffusion_chaleur_fil_homogene(Fil_Cuivre, r)
Testbench.plot_crepe()

Testbench.terminer()
r.terminer()

print(f"Programme executé en {'%.5s'%(time.time() - start_time)} secondes")