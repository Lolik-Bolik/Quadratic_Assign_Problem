from algorithms import LocalSearch, IteratedLocalSearch, GuidedLocalSearch
from utils import tools


reader = tools.QAReader()
data = reader('./data/tai20a')
searcher = GuidedLocalSearch(data, True, 50)
solution = searcher()
print(solution)