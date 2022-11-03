from mpi4py import MPI
import bcrypt

difficultyOfBcrypt = 14

def main():
    comm = MPI.COMM_WORLD
    id = comm.Get_rank()            #number of the process running the code
    numProcesses = comm.Get_size()  #total number of processes running
    myHostName = MPI.Get_processor_name()  #machine name running the code

    REPS = 10000

    if (numProcesses <= REPS):
      calculateHashes(range(id, REPS, numProcesses))

    else:
        # can't hove more processes than work; one process reports the error
        if id == 0 :
            print("Please run with number of processes less than \
or equal to {}.".format(REPS))

def calculateHashes(list):
  listHashes = []

  for text in list:
    salt = bcrypt.gensalt(difficultyOfBcrypt)
    password = bcrypt.hashpw(str(text).encode('utf-8'), salt)
    
    print("teste")
    listHashes.append(password)
