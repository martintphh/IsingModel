#from src.ising_model import IsingMetropolis_numba
from src.temperature_scan import temperature_scan
from src.visualizations import temperature_scan_plot
import argparse
import numpy as np
#import os

parser = argparse.ArgumentParser()
parser.add_argument("Tmin", help="the starting temperature of the scan", type=float)
parser.add_argument("Tmax", help="the final temperature of the scan", type=float)
parser.add_argument("--Tstep", help="temperature step size of the scan (default 0.2)", type=float, default=0.2)
parser.add_argument("--burn_in", help="time needed to reach equilibrium (default 2000)", type=int, default=2000)

parser.add_argument("N", help="size of the grid", type=int)
parser.add_argument("--J", help="coupling constant (default 1.)", type=float, default=1.)
parser.add_argument("--mu", help="chemical potential (default 0.)", type=float, default=0.)
parser.add_argument("--H", help="external magnetic field (default 0.)", type=float, default=0.)
parser.add_argument("--initial_spin_down", help="parts of spin down in the initial grid (default 0.5)", type=float, default=0.5)
parser.add_argument("--sweeps", help="number of Monte Carlo sweeps of the simulation (default 5000)", type=int, default=5000)
parser.add_argument("--save_as", help="if you want to save the image enter name here")

args = parser.parse_args()

#benötigt Tmin, Tmax, Tstep(mit default = 0.2)

temperatures = np.arange(args.Tmin, args.Tmax + 1e-9, args.Tstep)

parameter = {
    "N":args.N,
    "J": args.J,
    "mu": args.mu,
    "H": args.H,
    "initial_spin_down": args.initial_spin_down,
    "sweeps": args.sweeps}


def main():
    observables = temperature_scan(temperatures, burn_in=args.burn_in, **parameter)

    plot = temperature_scan_plot(temperatures=temperatures, observables=observables, save_path=args.save_as)
    return 0

if __name__=="__main__":
    main()
