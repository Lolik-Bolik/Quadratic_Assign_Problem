from algorithms import LocalSearch, IteratedLocalSearch, GuidedLocalSearch
from utils import tools
from os import listdir
from os.path import isfile, join
from os import path
import argparse

best_known = {
    'tai20a': 703482,
    'tai40a': 3139370,
    'tai60a': 7205962,
    'tai80a': 13499184,
    'tai100a': 21044752,
}


def main(args):
    reader = tools.QAReader()
    benchmarks = [f for f in listdir(args.path) if isfile(join(args.path, f))]
    for file in benchmarks:
        data = reader(path.join(args.path, file))
        searcher = GuidedLocalSearch(data, True, 20)
        solution = searcher()
        print(solution)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str,
                        help="path to benchmark data")
    args = parser.parse_args()
    main(args)

