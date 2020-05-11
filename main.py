import algorithms as algo
from utils import tools
from os import listdir
from os.path import isfile, join
from os import path
import argparse
import csv
import time

best_known = {
    'tai20a': 703482,
    'tai40a': 3139370,
    'tai60a': 7205962,
    'tai80a': 13499184,
    'tai100a': 21044752,
}


def main(args):
    if args.make_csv:
        with open('statistic.csv', 'w') as file:
            columns_names = ['File name', 'Method', 'Best known', 'Result', 'Time']
            writer = csv.DictWriter(file, fieldnames=columns_names)
            writer.writeheader()
            reader = tools.QAReader()
            benchmarks = [f for f in listdir(args.path) if isfile(join(args.path, f))]
            for file in benchmarks:
                data = reader(path.join(args.path, file))
                algorithms = [(name, f(data, '2-opt', True, 1)) for name, f in algo.__dict__.items() if callable(f)]
                for name, algorithm in algorithms:
                    print(f'{name} working on {file}')
                    start_time = time.time()
                    solution, final_cost = algorithm()
                    work_time = round(time.time() - start_time, 4)
                    writer.writerow({
                        'File name': file,
                        'Method': name,
                        'Best known': best_known[file],
                        'Result': final_cost,
                        'Time': work_time
                    })


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str,
                        help="path to benchmark data")
    parser.add_argument("-csv", "--make_csv", action='store_true',
                        help="path to benchmark data")
    args = parser.parse_args()
    main(args)

