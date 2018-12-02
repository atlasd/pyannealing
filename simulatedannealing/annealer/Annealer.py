import pandas as pd
import numpy as np
import tqdm

class Annealer:
    def __init__(self, f, alpha, beta, n_changes,
                epsilon, m0, neighbor,
                pchange=None, verbose=False):
        assert alpha < 1 and 0 < alpha, "Invalid value for alpha"

        self.alpha = alpha
        self.f = f
        self.beta = beta
        self.n_changes = n_changes
        self.epsilon = epsilon
        self.m = m0
        self.temp = 100
        self.neighbor = neighbor
        self.pchange = pchange
        self.best_solution = None
        self.verbose = verbose


    def get_pchange(self, f, temp, theta_t, new_theta):
        '''
        Parameters:
        -----------
        f : function
            The objective function

        temp : float
            The current temperature

        theta_t : np.ndarray
            The current state

        new_theta : np.ndarray
            The candidate state
        '''
        if self.pchange:
            return self.pchange(theta_t, new_theta)
        else:
            dist = f(theta_t) - f(new_theta)
            boltz = np.exp(dist / temp)
            return boltz if boltz < 1.0 else 1.0

    def update_temp(self):
        '''
        Update the temperature based on the
        given value of alpha
        '''
        self.temp = self.alpha * self.temp

    def update_m(self):
        '''
        Update the value of m based on the
        function beta assigned
        '''
        self.m = self.beta(self.m)

    def neighbor(self, theta):
        '''
        Uses the neighbor object to create a neighbor
        candidate solution.
        '''
        return self.neighbor.neighbor(theta, self.n_changes)

    def update_theta(self, theta):
        '''
        Updates the value of theta based on the value
        '''
        candidate = self.neighbor.neighbor(theta)
        cutoff = np.random.uniform(low=0.0, high=1.0, size=1)
        pmove = self.get_pchange(self.f, self.temp, theta, candidate)
        if cutoff <= pmove:
            return candidate
        else:
            return theta

    def run_iteration(self, theta0):
        '''
        Function to run m iterations of neighborhood and draw
        '''
        bar = tqdm.tqdm if self.verbose else lambda x: x
        for i in bar(range(int(self.m))):
            theta0 = self.update_theta(theta0)
            if self.best_solution is None:
                self.best_solution = theta0
            elif self.f(theta0) <= self.f(self.best_solution):
                    self.best_solution = theta0
        return theta0

    def run(self, theta0):
        while self.temp > self.epsilon:
            print(f"Running {self.m} Iterations")
            print(f"Current Temperature: {self.temp}")
            theta0 = self.run_iteration(theta0)
            self.update_m()
            self.update_temp()
            print(f"Best Solution: {self.f(self.best_solution)}")
        return self.best_solution
