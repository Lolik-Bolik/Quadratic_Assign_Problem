import numpy as np

__all__ = ['QAData', 'QAReader']


class QAData:
    def __init__(self, n, distances, flows):
        self.n = n
        self.distances = distances
        self.flows = flows
        self.solution = self.init_solution()

    def init_solution(self):
        return np.random.permutation(np.arange(self.n))

    def compute_cost(self):
        rows = np.arange(self.n)
        cost = (self.distances[rows, self.solution] * self.flows[rows, self.solution]).sum()
        return cost


class QAReader:
    def __init__(self):
        pass

    def __call__(self, path):
        print("Reading problem from {}".format(path))
        with open(path, "r") as f:
            n = int(f.readline().strip())
            distances, flows = np.empty((n, n)), np.empty((n, n))
            for i in range(n):
                flows[i] = (list(map(int, f.readline().split())))
            _ = f.readline()
            for j in range(n):
                distances[j] = (list(map(int, f.readline().split())))
        return QAData(n, distances, flows)


# reader = QAReader()
# data = reader('./data/tai20a')
# print(data.init_solution(), data.compute_cost())