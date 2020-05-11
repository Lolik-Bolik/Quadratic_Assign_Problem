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
        self.patience = int(0.2 * self.iter_amount)
        self.improved = True
        self.no_improvements = 0

    def stohastic_2_opt(self, **kwargs):
        if self.verbose:
            print(f'Starting value of cost func is {self.data.compute_cost(self.solution)}')

        for _ in tqdm(range(self.iter_amount), disable=not self.verbose):
            if not self.improved:
                self.no_improvements += 1
            if self.no_improvements == self.patience:
                break
            best_solution = self.solution
            self.improved = False
            for _ in range(int(0.2 * self.iter_amount)):
                ind_left = rd.randint(0, self.data.n - 1)
                ind_right = rd.randint(ind_left + 1, self.data.n)
                tmp_solution = self.solution.copy()
                tmp_solution[ind_left:ind_right] = tmp_solution[ind_left:ind_right][::-1]
                cost = self.data.compute_cost(tmp_solution, **kwargs)
                if cost < self.current_cost:
                    self.improved = True
                    self.no_improvements = 0
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
                diff += 2 * (self.data.flows[k, r]) * \
                        (self.data.distances[pi[k], pi[s]] - self.data.distances[pi[k], pi[r]]) + \
                        (self.data.flows[k, s]) * \
                        (self.data.distances[pi[k], pi[r]] - self.data.distances[pi[k], pi[s]])
        return diff

    def count_delta_with_previous(self, previous, u, v, r, s):
        pi = self.solution
        return previous + 2 * (self.data.flows[r, u] - self.data.flows[r, v] + self.data.flows[s, v] - self.data.flows[s, u]) * \
                          (self.data.distances[pi[s], pi[u]] - self.data.distances[pi[s], pi[v]] + self.data.distances[pi[r], pi[v]] - self.data.distances[pi[r], pi[u]])

    def first_improvement(self):
        if self.verbose:
            print(f'Starting value of cost func is {self.data.compute_cost(self.solution)}')

        dont_look_bits = np.zeros(self.data.n, dtype=np.bool)
        for _ in tqdm(range(self.iter_amount), disable=not self.verbose):
            comb = combinations(np.arange(self.data.n, dtype=np.int32), 2)
            if not self.improved:
                self.no_improvements += 1
            if self.no_improvements == self.patience or np.all(dont_look_bits):
                break
            self.improved = False
            curr_city = 0
            counter = 0
            for opt in comb:
                if dont_look_bits[opt[0]] or dont_look_bits[opt[1]]:
                    continue
                opt = list(opt)
                tmp_solution = self.solution.copy()
                tmp_solution[opt] = tmp_solution[opt][::-1]
                cost = self.data.compute_cost(tmp_solution)
                if curr_city != opt[0] and counter == self.data.n - 1 - curr_city:
                    # print(curr_city)
                    dont_look_bits[curr_city] = 1
                    curr_city += 1
                    counter = 0
                elif curr_city != opt[0]:
                    curr_city += 1
                    counter = 0
                if cost < self.current_cost:
                    self.improved = True
                    self.no_improvements = 0
                    self.current_cost = cost
                    self.solution = tmp_solution
                    # print(dont_look_bits)
                    break
                elif curr_city == opt[0]:
                    counter += 1


        final_cost = self.data.compute_cost(self.solution)
        if self.verbose:
            print('Final cost {}'.format(final_cost))
        return self.solution, final_cost

    def best_improvement(self):
        if self.verbose:
            print(f'Starting value of cost func is {self.data.compute_cost(self.solution)}')
        previous_opt = None
        previous_delta = None
        for _ in tqdm(range(self.iter_amount), disable=not self.verbose):
            comb = list(combinations(np.arange(self.data.n, dtype=np.int32), 2))
            if not self.improved:
                self.no_improvements += 1
            if self.no_improvements == self.patience:
                break
            self.improved = False
            min_delta = previous_delta if previous_delta is not None else 0
            optimal_opt = None
            for opt in comb:
                opt = list(opt)
                if previous_opt is not None and not opt == previous_opt:
                    delta = self.count_delta_with_previous(previous_delta, *opt, *previous_opt)
                elif opt == previous_opt:
                    continue
                else:
                    delta = self.count_delta(*opt)
                if delta < min_delta:
                    min_delta = delta
                    optimal_opt = opt
            if optimal_opt is not None:
                self.solution[optimal_opt] = self.solution[optimal_opt][::-1]
                self.improved = True
                previous_opt = optimal_opt
                previous_delta = min_delta
            else:
                self.improved = False
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


