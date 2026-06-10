from src.ising_model import IsingMetropolis_numba
from src.visualizations import time_plot
import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

parser.add_argument("N", help="size of the grid", type=int)
parser.add_argument("T", help="temperature at which the simulation will run", type=float)
parser.add_argument("--J", help="coupling constant (default 1.)", type=float, default=1.)
parser.add_argument("--mu", help="chemical potential (default 0.)", type=float, default=0.)
parser.add_argument("--H", help="external magnetic field (default 0.)", type=float, default=0.)
parser.add_argument("--initial_spin_down", help="parts of spin down in the initial grid (default 0.5)", type=float, default=0.5)
parser.add_argument("--sweeps", help="number of Monte Carlo sweeps of the simulation (default 5000)", type=int, default=5000)
parser.add_argument("--save_as", help="if you want to save the image enter name here")

args = parser.parse_args()






def main():
    model = IsingMetropolis_numba(args.N, args.T, args.J, args.mu, args.H, args.initial_spin_down, args.sweeps)
    model.run_simulation()

    E_expected = model.calculate_observables()["mean_e"]
    print(E_expected)

    plot = time_plot(model=model, save_path=args.save_as, window=150)

if __name__=="__main__":
    main()

