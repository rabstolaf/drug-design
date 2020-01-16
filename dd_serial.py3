# implementation of drug design exemplar
# serial, python3, introductory

import string
import random

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

# main program

random.seed(0) # guarantees that each run uses the same random number sequence
# parse command-line args...

# generate ligands
ligands = []
for l in range(nLigands):
    ligands.append(makeLigand(maxLigand))

# determine ligands with highest score
maxScore = -1
maxScoreLigands = []

for lig in ligands:
    s = score(lig, protein)
    if s > maxScore:
        maxScore = s
        maxScoreLigands = [lig]
        print("\n... new maxScore", s, "  ", lig, end='', flush=True) # show progress
    elif s == maxScore:
        maxScoreLigands.append(lig)
        print(", ", lig, end='', flush=True) # show progress
    

print()  # show progress
print('The maximum score is', maxScore)
print('Achieved by ligand(s)', maxScoreLigands)
