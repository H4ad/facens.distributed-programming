from math import floor
import genetic_algorithm

def geneticAlgorithm(ages, populationSize):
    initialPopulation = genetic_algorithm.getPopulation(populationSize)

    for age in range(ages):

        rankedSolutions = []

        for index, item in enumerate(initialPopulation, start=1):
            rankedSolutions.append(
                (genetic_algorithm.fitness(item[0], item[1], index), item, index)
            )

        print(f"=== Geração { age } best solutions ===")
        print(rankedSolutions[0])

        limit = floor(populationSize * 0.05)
        bestSolutions = genetic_algorithm.selection(rankedSolutions, limit)
        initialPopulation = genetic_algorithm.mutation(bestSolutions, populationSize)


# Variáveis
population = 1000
numAges = 10000

# Rodando o código
geneticAlgorithm(numAges, population)
