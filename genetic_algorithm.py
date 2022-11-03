from random import uniform, choice
import numpy as np

def objective(a, b, x):
    result = a * x + b

    # print(f"{a} * {x} + {b} = {result} => {x}")

    return result


def fitness(a, b, x):
    ans = objective(a, b, x)

    if ans > x:
        return abs(x / ans)
    else:
        return ans


def getPopulation(populationSize):
    population = []

    for _ in range(populationSize):
        population.append((uniform(0, populationSize), uniform(0, populationSize)))

    return population


def selection(rankedSolutions, limit):
    rankedSolutions.sort(reverse=True)

    return rankedSolutions[:limit]


def mutation(bestSolutions, populationSize):
    elements1 = []
    elements2 = []

    for element in bestSolutions:
        elements1.append(element[1][0])
        elements2.append(element[1][1])

    newPopulation = []

    for _ in range(populationSize):
        random1 = choice(elements1) * uniform(0.95, 1.05)
        random2 = choice(elements2) * uniform(0.95, 1.05)

        newPopulation.append((random1, random2))

    return newPopulation

# ref: https://stackoverflow.com/a/312464/8741188
def chunks(lst, n):
    return np.array_split(lst, n)

def log_normal(lvl, msg):
    if lvl >= 1:
      print(msg)

def log_info(lvl, msg):
    if lvl >= 2:
      print(msg)

def log_verbose(lvl, msg):
    if lvl >= 3:
        print(msg)
