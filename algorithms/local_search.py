from utils import tools
from tqdm import tqdm
import random as rd
import copy


class LocalSearch:
    def __init__(self, path_to_data, method, verbose, n_iter):
        reader = tools.QAReader()
        self.data = reader(path_to_data)
        self.method = method
        self.verbose = verbose
        self.iter_amount = n_iter
        self.solution = tools.init_solution(self.data.n)
        self.current_cost = self.data.compute_cost(self.solution)

    def stohastic_2_opt(self):
        if self.verbose:
            print(f'Starting value of cost func is {self.data.compute_cost(self.solution)}')
            print(f'Start solution is {self.solution}')
        for _ in tqdm(range(self.iter_amount), position=0, disable=not self.verbose):
            best_solution = self.solution
            for _ in range(self.iter_amount):
                ind_left = rd.randint(0, self.data.n - 1)
                ind_right = rd.randint(ind_left + 1, self.data.n)
                tmp_solution = copy.copy(self.solution)
                tmp_solution[ind_left:ind_right] = tmp_solution[ind_left:ind_right][::-1]
                cost = self.data.compute_cost(tmp_solution)
                if cost < self.current_cost:
                    self.current_cost = cost
                    best_solution = tmp_solution
            self.solution = best_solution
        final_cost = self.data.compute_cost(self.solution)
        if self.verbose:
            print('Final cost {}'.format(final_cost))
        return self.solution

    def __call__(self):
        if self.method == '2-opt':
            return self.stohastic_2_opt()
        elif self.method == 'first-improvement':
            pass
        else:
            pass


