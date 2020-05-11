import numpy as np

__all__ = ['QAData', 'QAReader', 'init_solution']


def init_solution(n):
    return np.random.permutation(np.arange(n))


class QAData:
    def __init__(self, n, distances, flows):
        self.n = n
        self.distances = distances
        self.flows = flows

    def compute_cost(self, solution, **kwargs):
        cost = 0
        for i in range(self.n):
            for j in range(self.n):
                dist = self.distances[solution[i]][solution[j]]
                flow = self.flows[i][j]
                cost += flow * dist

        if 'method' not in kwargs.keys():
            return cost
        elif kwargs['method'] == 'guided':
            augmented_part = 0
            mu = kwargs['mu']
            indicator_func = kwargs['indicator']
            penalty = kwargs['penalty']
            for u in range(self.n):
                for v in range(self.n):
                    augmented_part += indicator_func[u][v] * penalty[u][v]
            return cost + mu * augmented_part


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

