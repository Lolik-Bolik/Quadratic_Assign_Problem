from algorithms import LocalSearch, IteratedLocalSearch
from utils import tools


reader = tools.QAReader()
data = reader('./data/tai20a')
searcher = IteratedLocalSearch(data, True, 100)
solution = searcher()
print(solution)