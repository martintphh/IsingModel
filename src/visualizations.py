import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
from .find_burn_in import *


def time_plot(model, save_path=None, window=100):
    fig, ax = plt.subplots(1, 2, figsize=(12, 4), constrained_layout=True)
    e = np.array(model.energies)/(model.N**2)
    m = np.array(np.abs(model.magnetizations))/(model.N**2) #|m| not m
    
    e_smooth = moving_average(e, window)
    m_smooth = moving_average(m, window)
    t_smooth = np.arange(window - 1, model.sweeps)

    observables = model.calculate_observables()
    e_expected = observables["mean_e"]
    m_expected = observables["mean_m"]
    de = np.sqrt(observables["mean_e2"]-observables["mean_e"]**2)
    dm = np.sqrt(observables["mean_m2"]-observables["mean_m"]**2)


    print(f"<e> = {e_expected}")
    print(f"<m> = {m_expected}")
    print(f"sigma_e = {de}")
    print(f"sigma_m = {dm}")

    burn_in_e = find_burn_in(e_smooth, e_expected, de)
    burn_in_e_sweep = burn_in_e + window - 1
    burn_in_m = find_burn_in(m_smooth, m_expected, dm)
    burn_in_m_sweep = burn_in_m + window - 1

    recommended_burn_in = max(burn_in_e_sweep,burn_in_m_sweep)

    print(f"estimated burn ins: t_e = {burn_in_e_sweep}, t_b = {burn_in_m_sweep}\n")
    print(f"recommended burn: in t = {recommended_burn_in}")

    ax[0].plot(range(model.sweeps), e, label=r"$e(t)$", lw=0.7, alpha=0.25)
    ax[0].plot(t_smooth, e_smooth, label=r"moving average e(t)")
    ax[0].fill_between(range(model.sweeps), e_expected-de, e_expected+de,alpha=0.25, label=r"$\langle e \rangle \pm \sigma$")
    ax[0].axvline(x=burn_in_e_sweep, ymin=-2., ymax=1., color='gray', linestyle="--", lw=1.5, label=r"$t_{\mathrm{burn}}$")

    ax[0].set_xlabel(r"Monte Carlo sweep $t$")
    ax[0].set_ylabel(r"Energy per spin $e=E/(N^2J)$")

    ax[1].plot(range(model.sweeps), m, label=r"$|m(t)|$", lw=0.7, alpha=0.25)
    ax[1].plot(t_smooth, m_smooth, label=r"moving average m(t)")
    ax[1].fill_between(range(model.sweeps), m_expected-dm, m_expected+dm, alpha=0.25,label=r"$\langle m \rangle \pm \sigma_m$")
    ax[1].axvline(x=burn_in_m_sweep, color='gray', linestyle="--", lw=1.5, label=r"$t_{\mathrm{burn}}$")

    ax[1].set_xlabel(r"Monte Carlo sweep $t$")
    ax[1].set_ylabel(r"Magnetization per spin $m=M/(N^2J)$")

    ax[0].set_title(r"Energy relaxation")
    ax[1].set_title(r"Magnetization relaxation")

    ax[0].legend()
    ax[1].legend()
    if save_path:
        results_dir = os.path.join("..", "results")
        os.makedirs(results_dir, exist_ok=True)

        plt.savefig(os.path.join(results_dir, f"{save_path}.png"), dpi=300)
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
    
