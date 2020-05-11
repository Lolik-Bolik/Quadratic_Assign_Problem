from utils import tools
from tqdm import tqdm
import random as rd
from algorithms import LocalSearch
import copy
from itertools import combinations
import numpy as np


class GuidedLocalSearch:
    def __init__(self, data, method, verbose, n_iter):
        self.data = data
        self.verbose = verbose
        self.method = method
        self.iter_amount = n_iter
        self.solution = tools.init_solution(self.data.n)
        self.current_cost = self.data.compute_cost(self.solution)
        self.solver = LocalSearch(self.data, method, False, 10)
        self.penalty = np.zeros((self.data.n, self.data.n))
        self.indicator_func = np.zeros((self.data.n, self.data.n))
        self.params = {'method': 'guided', 'mu': 100, 'penalty': self.penalty,
                       'indicator': self.indicator_func}
        self.cost_history = []

    def cost_func(self, solution, u, v):
        cost = 0
        for i in range(self.data.n):
            cost += self.data.flows[u][i] * self.data.distances[v][solution[i]] if self.indicator_func[u][v] else 0
        return cost

    def utility_func(self, solution, u, v):
        return self.cost_func(solution, u, v) / (1 + self.penalty[u][v])

    def update_indicator(self, solution):
        self.indicator_func = np.zeros((self.data.n, self.data.n))
        for u in solution:
            for v in np.arange(self.data.n):
                self.indicator_func[v][u] = 1

    def __call__(self):
        if self.verbose:
            print(f'Starting value of cost func is {self.data.compute_cost(self.solution)}')
        for _ in tqdm(range(self.data.n)):
            max_util_index = None
            max_util_value = 0
            new_solution, new_cost_value = self.solver(self.solution, **self.params)
            self.cost_history.append(new_cost_value)
            self.update_indicator(new_solution)
            if new_cost_value < self.current_cost:
                self.solution = new_solution
                self.current_cost = new_cost_value
            for i in range(self.data.n):
                util_func_value = self.utility_func(new_solution, i, new_solution[i])
                if util_func_value > max_util_value:
                    max_util_value = util_func_value
                    max_util_index = i
            self.penalty[max_util_index][new_solution[max_util_index]] += 1
        final_cost = self.data.compute_cost(self.solution)
        if self.verbose:
            print('Final cost {}'.format(final_cost))
        return self.solution, final_cost


