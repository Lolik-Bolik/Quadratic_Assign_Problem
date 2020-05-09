import numpy as np


def get_problem_data(path):

    with open(path, 'r') as f:
        file = f.read().split('\n')

    n = int(file[0])
    distances = np.zeros((n, n), dtype=np.int32)
    flows = np.zeros((n, n), dtype=np.int32)
    for i in range(n):
        distances[i, :] = [int(x) for x in file[1+i].split(' ') if x]
        flows[i, :] = [int(x) for x in file[2+i+n].split(' ') if x]
    return dict(n=n,
                dists=distances,
                flows=flows)