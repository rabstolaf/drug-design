# implementation of drug design exemplar
# serial, python3, introductory

import string
import argparse
import random
import math
from multiprocessing import *

DFLT_nProcs = 4
DFLT_maxLigand = 5
DFLT_nLigands = 120
DFLT_protein = "the cat in the hat wore the hat to the cat hat party"

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

# function printIf - used for verbose output
#   variable number of arguments:  a boolean, then valid arguments for print
#   state change:  if arg1 is True, call print with the remaining arguments

def printIf(cond, *positionals, **keywords):
    if cond:
        print(*positionals, **keywords)

# function worker - code executed by each worker process
#   3 args:  a Queue for communication with main(),
#      parsed command-line arguments or defaults including protein,
#      and a list of ligands to score against that protein
#   state change:  a list having the form   [score, [ligand1, ligand2, ...]]
#      is put onto the Queue arg1, where score is the maximal score among
#      ligands in arg3 when compared against arg2.protein, and
#      ligand1, ligand2, ... are all ligands in arg3 achieving that score

def worker(q, args, ligandList):
    pid = current_process().pid
    maxScore = -1
    maxScoreLigands = []

    for lig in ligandList:
        s = score(lig, args.protein)
        if s > maxScore:
            maxScore = s
            maxScoreLigands = [lig]
            printIf(args.verbose, "\n[{}]-->new maxScore {}".format(pid, s))
            printIf(args.verbose, "[{}]{}, ".format(pid, lig),
                    end='', flush=True) 
        elif s == maxScore:
            maxScoreLigands.append(lig)
            printIf(args.verbose, "[{}]{}, ".format(pid, lig),
                    end='', flush=True) 
    
    printIf(args.verbose)  # print final newline
    q.put([maxScore, maxScoreLigands])


# main program

def main():
    random.seed(0) # guarantees that each run uses same random number sequence

    # parse command-line args...
    parser = argparse.ArgumentParser(
        description="CSinParallel Drug Design simulation - sequential")
    parser.add_argument('maxLigand', metavar='max-length', type=int, nargs='?',
        default=DFLT_maxLigand, help='maximum length of a ligand')
    parser.add_argument('nLigands', metavar='count', type=int, nargs='?',
        default=DFLT_nLigands, help='number of ligands to generate')
    parser.add_argument('nProcs', metavar='threads', type=int, nargs='?',
        default=DFLT_nProcs, help='number of processes to generate')
    parser.add_argument('protein', metavar='protein', type=str, nargs='?',
        default=DFLT_protein, help='protein string to compare ligands against')
    parser.add_argument('-verbose', action='store_const', const=True,
                        default=False, help='print verbose output')
    args = parser.parse_args()    # parse command-line args...

    # generate ligands
    ligands = []
    for l in range(args.nLigands):
        ligands.append(makeLigand(args.maxLigand))

    # determine ligands with highest score
    maxScore = -1
    maxScoreLigands = []

    q = Queue()
    workers = []
    n = math.ceil(len(ligands)/args.nProcs) # ligands per worker
    for p in range(args.nProcs):
        proc = Process(target=worker, args=(q, args, ligands[p*n:(p+1)*n]))
        workers.append(proc)
        proc.start()
    for p in workers:
        p.join()
        msg = q.get()
        if msg[0] > maxScore:
            maxScore = msg[0]
            maxScoreLigands = msg[1]
        elif msg[0] == maxScore:
            maxScoreLigands = maxScoreLigands + msg[1]

    # print results
    print('The maximum score is', maxScore)
    print('Achieved by ligand(s)', maxScoreLigands)

main()
