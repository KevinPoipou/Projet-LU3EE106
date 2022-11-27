import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def get_diff(M_Temp, sub) :
    return np.subtract(M_Temp, sub)


def get_lim(M_Temp) :
    Tmin = np.amin(M_Temp)
    Tmax = np.amax(M_Temp)
    return Tmin, Tmax


def plot_crepe(M_Temp, Fil, dx, t_max, dt, autocolor=False, allowDifference=False) :
    """
    Retourne la matrice des temperatures (comme une crepe) et l'affiche -- Resulte un empilement de plusieurs fils
    """
    graph_titre = 'Diffusion de la chaleur dans un fil mis en pile'
    path = '../exports/figures/' + graph_titre + '.png'
    cmap = plt.get_cmap('jet')
    
    fig, ax = plt.subplots()

    nt = int(t_max / dt)
    nx = int(Fil.longx / dx)
    M_Temp = np.memmap('../datas/tmp/Diffusion_chaleur_mono.mm', dtype=np.float32, mode='r', shape=(nt, nx))

    Tmin, Tmax = get_lim(M_Temp)
    if(allowDifference) and (Tmax - Tmin < 1) :
        M_Temp = get_diff(M_Temp, Tmin)
        Tmin, Tmax = get_lim(M_Temp)
        print('Difference')
    
    vmin = 280    # Couleur minimum associe
    vmax = 400    # Couleur maximum associe
    if(autocolor == True) :
        vmin = Tmin
        vmax = Tmax

    print(vmin, vmax)

    im = ax.imshow(M_Temp, cmap=cmap, vmin=vmin, vmax=vmax, aspect='auto')
    ax.invert_yaxis()
    
    label_x = np.arange(0, int(Fil.longx/dx)+1, (2*Fil.longx)/(Fil.longx*dx))
    label_y = np.arange(0, int(t_max/dt)+1, (2*t_max)/(t_max*dt))
    
    ax.set_xticks(label_x, ['%d' %val for val in label_x * dx])
    ax.set_yticks(label_y, ['%.1f' %val for val in label_y * dt])
    
    ax.set(title=graph_titre, xlabel='Distance fil', ylabel='Temps')
    plt.colorbar(im, ax=ax, label = 'Temperature', ticks=np.linspace(vmin, vmax, 10), format='%.6f') #Affiche une bar de couleur

    fig.set_figheight(10)
    fig.set_figwidth(16)
    fig.savefig(path, dpi=300, bbox_inches = "tight")
    print('Image créée à', path)
    
    plt.show()


# def get_animation(mat, f_time, lfil, autocolor=False) :
#     """
#     Creer et enregistre une animation 1D
#     """
#     fig, ax = plt.subplots()
#     vmin = 280    # Couleur minimum associe
#     vmax = 400    # Couleur maximum associe
    
#     if(autocolor == True) :
#         vmin = np.amin(mat)
#         vmax = np.amax(mat)
        
#     ims = []
#     t = np.arange(0, f_time)
#     cmap = plt.get_cmap('jet')
#     for i in range(t.size-1):
#         im = ax.imshow(mat[i, :].reshape(1, lfil), animated=True, cmap=cmap, vmin=vmin, vmax=vmax)
#         #ax.set(title=f"i = {i}", xlabel='Distance fil', ylabel=f'Temps')
#         if i == 0:
#             ax.imshow(mat[i, :].reshape(1, lfil), cmap = cmap, vmin=np.amin(mat), vmax=np.amax(mat))  # show an initial one first
        
#         if(i == int(t.size/4)-1):
#             print('25%')
#         if(i == int(t.size/2)-1):
#             print('50%')
#         if(i == int(3*t.size/4)-1):
#             print('75%')
#         if(i == int(t.size)-2):
#             print('100%')
        
#         ims.append([im])
    
#     print('Animation')
#     ani = animation.ArtistAnimation(fig, ims, interval=1, blit=True,
#                                     repeat_delay=1000)
    
#     ani_titre = 'Diffusion de la chaleur dans un fil'
#     path = '../exports/animations/' + ani_titre + '.gif'
#     ani.save(path)
#     print('Animation créée à', path)
