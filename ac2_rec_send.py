import math
from mpi4py import MPI
import genetic_algorithm

# Variáveis
# controla a porcentagem de qnts vão ser usados para mutar após treinar
pickTopNByPercentageToMutate = 0.05
populationSize = 1000  # controla o tamanho da população
ages = 10000  # controla o número de ages que irá rodar

# NONE = 0
# NORMAL = 1
# INFO = 2
# VERBOSE = 3
logLevel = 0

def handleMaster(comm, numSlaves):
    initialPopulation = genetic_algorithm.getPopulation(populationSize)

    genetic_algorithm.log_normal(
        logLevel, "master(): Começando a treinar as gerações.")

    for age in range(ages):

        bestSolutions = []
        chunksToSlave = genetic_algorithm.chunks(initialPopulation, numSlaves)

        for slaveId, chunk in enumerate(chunksToSlave, start=1):
            genetic_algorithm.log_info(
                logLevel, f"master(Geração { age }): Enviando { len(chunk) } para slave({ slaveId })")

            # envia uma lista de população para ser treinada
            comm.send(chunk, dest=slaveId)

        genetic_algorithm.log_info(
            logLevel, f"master(Geração { age }): Valores enviados, aguardando recebimento.")

        for slaveId, _ in enumerate(chunksToSlave, start=1):
            # recebe o resultado com os melhores valores já selecionados
            slaveBestSolutions = comm.recv(source=slaveId)

            genetic_algorithm.log_info(
                logLevel, f"master(Geração { age }): Recebido { len(slaveBestSolutions) } de slave({ slaveId })")

            bestSolutions.extend(slaveBestSolutions)

        bestSolutions.sort(reverse=True)

        if age % 10 == 0:
            genetic_algorithm.log_normal(
                logLevel, f"=== Geração { age } best solution ===")
            genetic_algorithm.log_normal(
            logLevel, bestSolutions[0])

        initialPopulation = genetic_algorithm.mutation(
            bestSolutions, populationSize)


def handleSlave(comm, id):
    for age in range(ages):

        partOfPopulation = comm.recv(source=0)

        genetic_algorithm.log_info(
            logLevel, f"slave({ id }): Treinando geração {age} com { len(partOfPopulation) } items")

        rankedSolutions = []

        for index, item in enumerate(partOfPopulation, start=1):
            xValueToTest = len(partOfPopulation) * (id - 1) + index

            rankedSolutions.append(
                (genetic_algorithm.fitness(
                    item[0], item[1], xValueToTest), item, xValueToTest)
            )

        rankedSolutions.sort(reverse=True)

        selectTopN = math.floor(
            len(partOfPopulation)
            * pickTopNByPercentageToMutate
        )

        bestSolutions = genetic_algorithm.selection(
            rankedSolutions,
            selectTopN
        )

        genetic_algorithm.log_info(
            logLevel, f"slave({ id }): Melhor valor {rankedSolutions[0]} da geração {age}")

        # total = count_primes(receivedValue)

        # print("Process {} of {} received {}, number of primes is {}"
        #   .format(id, numProcesses, receivedValue, total))

        comm.send(bestSolutions, dest=0)


def main():
    comm = MPI.COMM_WORLD
    id = comm.Get_rank()  # number of the process running the code
    numProcesses = comm.Get_size()  # total number of processes running
    myHostName = MPI.Get_processor_name()  # machine name running the code

    numSlaves = numProcesses - 1

    genetic_algorithm.log_normal(logLevel, f"node({id}): Começando a rodar...")

    if numProcesses > 1:
        if id == 0:
            handleMaster(comm, numSlaves)
        else:
            handleSlave(comm, id)
    else:
        print("Please run this program with 2 processes at least")


main()
