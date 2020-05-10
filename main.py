from algorithms import LocalSearch


searcher = LocalSearch('./data/tai20a', 'best-improvement', True, 100)
solution = searcher()
print(solution)