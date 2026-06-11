import numpy as np
from numba import njit

@njit
def calculate_E(N, J, mu, H, grid):
    E = 0
    for x in range(N):
        for y in range(N):
            r = (x+1) % N
            d = (y+1) % N
            E -= J * grid[x,y] * (grid[x,d] + grid[r,y]) 
            E -= mu * H * grid[x,y] 
    return E


@njit
def run_simulation_numba(E, M, grid, T, J, mu, H, N, sweeps, save_grids=False, save_every=1):
    energies = np.empty(sweeps)
    magnetizations = np.empty(sweeps)
    
    grids = []
    saved_sweeps = []

    for time_step in range(sweeps):
        for spin in range(N**2):
            x, y = np.random.randint(0,N), np.random.randint(0,N)
            l = (x-1) % N
            r = (x+1) % N
            u = (y-1) % N
            d = (y+1) % N
            old_spin = grid[x,y]
            dE = 2 * J * grid[x,y] * (grid[l,y] + grid[r,y] + grid[x,u] + grid[x,d]) + 2 * H * mu * grid[x,y]
            if np.random.rand() < np.minimum(1, np.exp(-dE/T)):
                grid[x,y] *= -1
                E += dE
                M -= 2 * old_spin
        energies[time_step] = E
        magnetizations[time_step] = M
        if save_grids and (time_step + 1) % save_every == 0:
            grids.append(grid.copy())
            saved_sweeps.append(time_step + 1)
            

    return grid, E, M, energies, magnetizations, grids, saved_sweeps



class IsingMetropolis_numba:
    def __init__(self, N: int, T: float, J: float, mu: float, H: float, initial_spin_down: float, sweeps: int, save_grids: bool, save_every: int =1):
        self.N = N
        self.T = T
        self.J = J 
        self.mu = mu
        self.H = H 
        self.initial_spin_down = initial_spin_down
        self.sweeps = sweeps
        self.save_grids = save_grids
        self.saved_sweeps = []
        self.save_every = save_every

        self.grid = self.initialize_grid()
        self.E = self.calculate_energy()
        self.M = self.calculate_magnetization()
        self.grids = []
        self.energies = []
        self.magnetizations = []

        
        

    def initialize_grid(self):
        return np.where(np.random.rand(self.N, self.N) < self.initial_spin_down, -1,1)


    def run_simulation(self):
        self.grid, self.E, self.M, self.energies, self.magnetizations, self.grids, self.saved_sweeps = run_simulation_numba(
            self.E,
            self.M,
            self.grid,
            self.T,
            self.J,
            self.mu,
            self.H,
            self.N,
            self.sweeps,
            self.save_grids,
            self.save_every
        )

    def calculate_energy(self):
        return calculate_E(self.N, self.J, self.mu, self.H, self.grid)
        

    def calculate_magnetization(self):
        return np.sum(self.grid)

    def calculate_observables(self, burn_in=1000):
        E = np.array(self.energies[burn_in:])
        M = np.array(self.magnetizations[burn_in:])

        e = E/(self.N**2)
        m = M/(self.N**2)

        return {
            "mean_e": np.mean(e),
            "mean_e2": np.mean(e**2),
            "mean_m": np.mean(m),
            "mean_m2": np.mean(m**2),
            "mean_abs_m": np.mean(np.abs(m)),
            "mean_abs_m2": np.mean(np.abs(m)**2)
        }

    
  
