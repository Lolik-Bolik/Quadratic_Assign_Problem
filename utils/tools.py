import numpy as np

__all__ = ['QAData', 'QAReader']


class QAData:
    def __init__(self, n, distances, flows):
        self.n = n
        self.distances = distances
        self.flows = flows


class QAReader:
    def __init__(self):
        pass

    def __call__(self, problem_filepath, *args, **kwargs):
        print("Reading problem from {}".format(problem_filepath))
        with open(problem_filepath, "r") as f:
            n = int(f.readline().strip())
            distances, flows = np.empty((n, n)), np.empty((n, n))
            for i in range(n):
                flows[i] = (list(map(int, f.readline().split())))
            _ = f.readline()
            for j in range(n):
                distances[j] = (list(map(int, f.readline().split())))
        return QAData(n, distances, flows)

