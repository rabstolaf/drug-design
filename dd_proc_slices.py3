# implementation of drug design exemplar
# serial, python3, introductory

import string
import random
from multiprocessing import *
import math

maxLigand = DEFAULT_max_ligand = 5
nLigands = DEFAULT_nligands = 120
nThreads = DEFAULT_nthreads = 4
protein = DEFAULT_protein = \
    "the cat in the hat wore the hat to the cat hat party"

# function makeLigand
#   1 argument:  maximum length of a ligand
#   return:  a random ligand string of random length between 1 and arg1

def makeLigand(maxLength):
    len = random.randint(1, maxLength)
    ligand = ""
    for c in range(len):
        ligand = ligand + string.ascii_lowercase[random.randint(0,25)]
    return ligand

# function score
#   2 arguments:  a ligand and a protein sequence
#   return:  int, simulated binding score for ligand arg1 against protein arg2

def score(lig, pro):
    if len(lig) == 0 or len(pro) == 0:
        return 0
    if lig[0] == pro[0]:
        return 1 + score(lig[1:], pro[1:])
    else:
        return max(score(lig[1:], pro), score(lig, pro[1:]))

def worker(q, ligandList):
    pid = current_process().pid
    maxScore = -1
    maxScoreLigands = []

    for lig in ligandList:
        s = score(lig, protein)
        if s > maxScore:
            maxScore = s

            maxScoreLigands = [lig]
            print("\n[", pid, "]-->new maxScore ", s, sep='') # show progress
            print("[", pid, ']', lig, ', ',
                  sep='', end='', flush=True) # show progress
        elif s == maxScore:
            maxScoreLigands.append(lig)
            print("[", pid, ']', lig, ', ',
                  sep='', end='', flush=True) # show progress
    
    print()  # show progress
    #return str(maxScore) + " " + ' '.join(maxScoreLigands)
    q.put([maxScore, maxScoreLigands])


# main program

random.seed(0) # guarantees that each run uses the same random number sequence
# parse command-line args...

# generate ligands
ligands = []
for l in range(nLigands):
    ligands.append(makeLigand(maxLigand))

# determine ligands with highest score
#ret = worker(ligands).split(' ', 1)
maxScore = -1
maxScoreLigands = []

q = Queue()
workers = []
n = math.ceil(len(ligands)/nThreads) # ligands per worker
for p in range(nThreads):
    proc = Process(target=worker, args=(q, ligands[p*n:(p+1)*n]))
    workers.append(proc)
    proc.start()
for w in workers:
    w.join()
    ret = q.get()
    if ret[0] > maxScore:
        maxScore = ret[0]
        maxScoreLigands = maxScoreLigands + ret[1]
    elif ret[0] == maxScore:
        maxScoreLigands = maxScoreLigands + ret[1]

# print results
print('The maximum score is', maxScore)
print('Achieved by ligand(s)', maxScoreLigands)
