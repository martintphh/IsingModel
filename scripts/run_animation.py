import argparse
from src.visualizations import animate_ising
from src.ising_model import IsingMetropolis_numba

parser = argparse.ArgumentParser()

parser.add_argument("N", help="size of the grid", type=int)
parser.add_argument("T", help="temperature at which the simulation will run", type=float)
parser.add_argument("--J", help="coupling constant (default 1.)", type=float, default=1.)
parser.add_argument("--mu", help="chemical potential (default 0.)", type=float, default=0.)
parser.add_argument("--H", help="external magnetic field (default 0.)", type=float, default=0.)
parser.add_argument("--initial_spin_down", help="parts of spin down in the initial grid (default 0.5)", type=float, default=0.5)
parser.add_argument("--sweeps", help="number of Monte Carlo sweeps of the simulation (default 5000)", type=int, default=5000)
parser.add_argument("--save_as", help="if you want to save the image enter name here")
parser.add_argument("--interval", help="time between frames in ms", type=int, default=100)
parser.add_argument("--save_every", help="save one grid every n sweeps for the animation", type=int, default=1)
args = parser.parse_args()



def main():
    model = IsingMetropolis_numba(args.N, args.T, args.J, args.mu, args.H, args.initial_spin_down, args.sweeps, save_grids=True, save_every=args.save_every)
    print("Running simulation...")
    model.run_simulation()
    print("Simulation finished.")
    print("Creating animation...")

    grids = model.grids
    sweep_numbers = model.saved_sweeps

    animation = animate_ising(
    grids,
    sweep_numbers=sweep_numbers,
    interval=args.interval,
    save_path=args.save_as
)
    print("Done.")

if __name__=="__main__":
    main()