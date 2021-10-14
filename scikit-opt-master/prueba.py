# step1: define your own operator:
def selection_tournament(algorithm, tourn_size):
    FitV = algorithm.FitV
    sel_index = []
    for i in range(algorithm.size_pop):
        aspirants_index = np.random.choice(range(algorithm.size_pop), size=tourn_size)
        sel_index.append(max(aspirants_index, key=lambda i: FitV[i]))
    algorithm.Chrom = algorithm.Chrom[sel_index, :]  # next generation
    return algorithm.Chrom


# %% step2: import package and build ga, as usual.
import numpy as np
from sko.GA import GA, GA_TSP


def demo_func(x):
    salida=5
    for i in range(len(x)-1):
        salida+=(x[i]-(1/x[i+1]))**2
    return salida

lower_bound=[]
upper_bound=[]
pres=[]
for i in range(86):
    lower_bound.append(1)
    upper_bound.append(5)
    pres.append(0.1)

ga = GA(func=demo_func, n_dim=86, size_pop=100, max_iter=500, prob_mut=0.001,
        lb=lower_bound, ub=upper_bound, precision=pres)

# %% step3: register your own operator
ga.register(operator_name='selection', operator=selection_tournament, tourn_size=3)
# %% Or import the operators scikit-opt already defined.
from sko.operators import ranking, selection, crossover, mutation

ga.register(operator_name='ranking', operator=ranking.ranking). \
    register(operator_name='crossover', operator=crossover.crossover_2point). \
    register(operator_name='mutation', operator=mutation.mutation)
# %% Run ga
best_x, best_y = ga.run()

print(best_x)
print(best_y)