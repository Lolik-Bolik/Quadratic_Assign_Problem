from utils import tools
from tqdm import tqdm
import random as rd
import copy
from itertools import combinations
import numpy as np


class LocalSearch:
    def __init__(self, data, method, verbose, n_iter, solution=None):
        self.data = data
        self.method = method
        self.verbose = verbose
        self.iter_amount = n_iter
        self.solution = tools.init_solution(self.data.n)
        self.current_cost = self.data.compute_cost(self.solution)

    def stohastic_2_opt(self, **kwargs):
        if self.verbose:
            print(f'Starting value of cost func is {self.data.compute_cost(self.solution)}')
        for _ in tqdm(range(self.iter_amount), disable=not self.verbose):
            best_solution = self.solution
            for _ in range(self.iter_amount):
                ind_left = rd.randint(0, self.data.n - 1)
                ind_right = rd.randint(ind_left + 1, self.data.n)
                tmp_solution = copy.copy(self.solution)
                tmp_solution[ind_left:ind_right] = tmp_solution[ind_left:ind_right][::-1]
                cost = self.data.compute_cost(tmp_solution, **kwargs)
                if cost < self.current_cost:
                    self.current_cost = cost
                    best_solution = tmp_solution
            self.solution = best_solution
        final_cost = self.data.compute_cost(self.solution, **kwargs)
        if self.verbose:
            print('Final cost {}'.format(final_cost))
        return self.solution, final_cost

    def count_delta(self, r, s):
        diff = 0
        pi = self.solution
        for k in range(self.data.n):
            if k != r and k != s:
                diff += (self.data.flows[k, r] + self.data.flows[r, k]) * \
                        (self.data.distances[pi[s], pi[k]] - self.data.distances[pi[r], pi[k]]) + \
                        (self.data.flows[k, s] + self.data.flows[s, k]) * \
                        (self.data.distances[pi[r], pi[k]] - self.data.distances[pi[s], pi[k]])
        return diff

    def first_improvement(self):
        if self.verbose:
            print(f'Starting value of cost func is {self.data.compute_cost(self.solution)}')

        comb = list(combinations(np.arange(self.data.n, dtype=np.int32), 2))
        dont_look_bits = np.zeros(self.data.n, dtype=np.bool)
        for i in tqdm(range(self.iter_amount)):
            curr_city = 0
            counter = 0
            for opt in comb:
                if dont_look_bits[opt[0]] or dont_look_bits[opt[1]]:
                    continue
                opt = list(opt)
                tmp_solution = copy.copy(self.solution)
                tmp_solution[opt] = tmp_solution[opt][::-1]
                cost = self.data.compute_cost(tmp_solution)
                if cost < self.current_cost:
                    self.current_cost = cost
                    self.solution = tmp_solution
                    break
                if curr_city == opt[0]:
                    counter += 1
                elif curr_city != opt[0] and counter == self.data.n - 1 - curr_city:
                    dont_look_bits[curr_city] = 1
                    curr_city += 1
                    counter = 0
                else:
                    curr_city += 1
                    counter = 0

        final_cost = self.data.compute_cost(self.solution)
        if self.verbose:
            print('Final cost {}'.format(final_cost))
        return self.solution, final_cost

    def best_improvement(self):
        if self.verbose:
            print(f'Starting value of cost func is {self.data.compute_cost(self.solution)}')
        comb = list(combinations(np.arange(self.data.n, dtype=np.int32), 2))
        for _ in tqdm(range(self.iter_amount)):
            min_delta = 0
            optimal_opt = None
            for opt in comb:
                opt = list(opt)
                delta = self.count_delta(*opt)
                if delta < min_delta:
                    min_delta = delta
                    optimal_opt = opt
            self.solution[optimal_opt] = self.solution[optimal_opt][::-1]
        final_cost = self.data.compute_cost(self.solution)
        if self.verbose:
            print('Final cost {}'.format(final_cost))
        return self.solution, final_cost

    def __call__(self, solution=None, **kwargs):
        if solution is not None:
            self.solution = solution
        if self.method == '2-opt':
            return self.stohastic_2_opt(**kwargs)
        elif self.method == 'first-improvement':
            return self.first_improvement()
        else:
            return self.best_improvement()


