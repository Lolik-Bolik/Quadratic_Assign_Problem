from utils import tools
from tqdm import tqdm
import random as rd
from algorithms import LocalSearch
import numpy as np


class IteratedLocalSearch:
    def __init__(self, data, method, verbose, n_iter):
        self.data = data
        self.verbose = verbose
        self.method = method
        self.iter_amount = n_iter
        self.solution = tools.init_solution(self.data.n)
        self.current_cost = self.data.compute_cost(self.solution)
        self.solver = LocalSearch(self.data, method, False, 20)
        self.cost_history = []

    def perturbation(self):
        k = rd.randint(2, self.data.n)
        indexes = np.random.choice(np.arange(self.data.n), k, replace=False)
        shuffled_indexes = np.random.permutation(indexes)
        new_solution = self.solution.copy()
        new_solution[indexes] = self.solution[shuffled_indexes]
        return new_solution

    def acceptance_criterion(self, new_solution):
        if self.data.compute_cost(self.solution) > self.data.compute_cost(new_solution):
            self.solution = new_solution

    def __call__(self):
        if self.verbose:
            print(f'Starting value of cost func is {self.data.compute_cost(self.solution)}')
        self.solution, cost = self.solver(self.solution)
        for _ in tqdm(range(self.iter_amount)):
            new_solution, cost = self.solver(self.perturbation())
            self.cost_history.append(cost)
            self.acceptance_criterion(new_solution)
        final_cost = self.data.compute_cost(self.solution)
        if self.verbose:
            print('Final cost {}'.format(final_cost))
        return self.solution, final_cost
