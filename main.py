from algorithms import LocalSearch


searcher = LocalSearch('./data/tai20a', '2-opt', True, 100)
solution = searcher()
print(solution)