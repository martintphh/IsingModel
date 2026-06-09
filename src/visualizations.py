import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os




def time_plot(model, save=False):
    fig, ax = plt.subplots(1, 2)
    e = np.array(model.energies)/(model.N**2)
    m = np.array(model.magnetizations)/(model.N**2)
    
    ax[0].plot(range(model.sweeps), e, label="e(t)", marker=".")
    ax[0].set_xlabel("x-achse")
    ax[0].set_ylabel("y-achse")

    ax[1].plot(range(model.sweeps), m, label="m(t)", marker=".")
    ax[1].set_xlabel("x-achse")
    ax[1].set_ylabel("y-achse")

    plt.legend()
    if save==True:
        plt.savefig("time_evolution.png", dpi=300)
    plt.show()
    return None
    


def temperature_scan_plot(temperatures, observables, save_path=None):
    fig, ax = plt.subplots(2,2)
    ax[0,0].scatter(temperatures, observables[0], label="C_V", marker=".")
    ax[0,1].scatter(temperatures, observables[1], label="chi", marker=".")
    ax[1,0].scatter(temperatures, observables[2], label="<e>", marker=".")
    ax[1,1].scatter(temperatures, observables[3], label="<m>", marker=".")

    plt.legend()
    if save_path:
        results_dir = os.path.join("..", "results")
        os.makedirs(results_dir, exist_ok=True)

        plt.savefig(os.path.join(results_dir, f"{save_path}.png"), dpi=300)
    plt.show()
    return None



def animate_ising(grids, interval=100, save=False):
    fig, ax = plt.subplots()
    
    im = ax.imshow(grids[0], vmin=-1, vmax=1)
    ax.set_title("Ising Model Evolution")

    def update(frame):
        im.set_data(grids[frame])
        ax.set_title(f"Sweep {frame}")
        return [im]

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(grids),
        interval=interval,
        blit=True
    )
    if save==True:
        ani.save("ising4.gif", writer="pillow")
    plt.show()
    return ani

#ani = animate_ising(grids)
#from IPython.display import HTML
#HTML(ani.to_jshtml())
    
