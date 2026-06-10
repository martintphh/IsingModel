import numpy as np
from .ising_model import IsingMetropolis_numba
from tqdm import tqdm



def temperature_scan(temperatures: list, burn_in=1000, **params):
    C_V = []
    chi = []
    e_mean = []
    m_mean_abs = []
    #for T in temperatures:
    for T in tqdm(temperatures, desc="Temperature scan"):
        model = IsingMetropolis_numba(
            N = params["N"],
            T = T,
            J = params["J"],
            mu = params["mu"],
            H = params["H"],
            initial_spin_down = params["initial_spin_down"],
            sweeps = params["sweeps"],
        )
        model.run_simulation()
        observables = model.calculate_observables(burn_in=burn_in)

        C_V.append((model.N**2)/(model.T**2)*(observables["mean_e2"] - observables["mean_e"]**2))
        chi.append((model.N**2)/(model.T)*(observables["mean_m2"] - observables["mean_abs_m"]**2))
        e_mean.append(observables["mean_e"])
        m_mean_abs.append(observables["mean_abs_m"])


    return [C_V, chi, e_mean, m_mean_abs]


