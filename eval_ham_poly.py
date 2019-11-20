#!/usr/bin/python

import argparse
from typing import List, Dict, Tuple, Any
from itertools import permutations
from pyfinite import ffield
import numpy as np

def bruteForceAssignments(n: int, l: int) -> np.ndarray:
    """
        n: The number of vertices in the complete graph in question
        l: F_2^l is the field we're working with
    """


    m = n**2 #edges
    q = 2**l #field size
    K = q**m 

    for num in range(K):
        X = np.ndarray((m), dtype = int)
        for i in range(m):
            X[i] = num & q-1
            num = num >> l
        X = np.reshape(X,(n,n))
        yield X

def randomAssignments(n: int, l: int, R: int, nonzero=False) -> np.ndarray:
    """
        n: The number of vertices in the complete graph in question
        l: F_2^l is the field we're working with
        R: the number of random matrices we ultimately want to draw
    """

    m = n**2 #edges
    q = 2**l #field size

    if nonzero is False:
        for i in range(R):
            X = np.random.randint(0,high=q,size=(n,n),dtype=int)
            yield X
    else:
        for i in range(R):
            X = np.random.randint(1,high=q,size=(n,n),dtype=int)
            yield X
       
def testEvaluations(n: int, l: int, mode: str, R=None, omit_zero=True):
    """
        n: The number of vertices in the complete graph in question
        l: F_2^l is the field we're working with


        Returns and prints the fraction of assignments over F_2^l to the
        edges of the complete graph K_n that yield a nonzero output. 
    """
    m = n**2 #edges
    q = 2**l #field size
    K = q**m 
    F = ffield.FField(l)

    zero_count = 0

    """
        K is an ml bit number. We want to split it up into l bit parts
        To do this, we pick a K, get just the last l bits by taking the AND with 
        q-1 (which is l 1's) and then rightshifting to get the next l bits. 
    """


    #Idea - precompute all the possible relevant monomial values and store them. 
    #Idea - do changes to the unvisited set using sortedcontainers

    if mode == "random":
        assert(R is not None)
        for X in randomAssignments(n,l,R,omit_zero):
            evaluation = 0
            for perm in permutations(list(range(1,n))):
                monomial = X[0,perm[0]]
                vtx = 0
                for i in range(n-1):
                    monomial = F.Multiply(monomial, X[vtx,perm[i]])
                    vtx = perm[i]
                monomial = F.Multiply(monomial, X[perm[n-2],0])
                evaluation = F.Add(monomial,evaluation)
            if evaluation == 0:
                zero_count += 1
        print("When n = ", n, "and l = ", l, "the fraction of nonzeros was: ", 1-float(zero_count)/R)

    else:
        for X in bruteForceAssignments(n,l):
            evaluation = 0
            for perm in permutations(list(range(1,n))):
                monomial = X[0,perm[0]]
                vtx = 0
                for i in range(n-1):
                    monomial = F.Multiply(monomial, X[vtx,perm[i]])
                    vtx = perm[i]
                monomial = F.Multiply(monomial, X[perm[n-2],0])
                evaluation = F.Add(monomial,evaluation)
            if evaluation == 0:
                zero_count += 1
        print("When n = ", n, "and l = ", l, "the fraction of nonzeros was: ", 1-float(zero_count)/K)

   
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--n_low", default = 3, type = int, action = "store", help = "smallest K_n to try")
    parser.add_argument("--l_low", default = 2, type = int, action = "store", help = "smallest F_2^l to try")
    parser.add_argument("--l_high", type = int, action = "store", help = "largest F_2^l to try")
    parser.add_argument("--n_high", type = int, action = "store", help = "largest K_n to try")
    parser.add_argument("--assign_mode", default = "random", type = str, action = "store", help = "how to assign variables")
    parser.add_argument("--num_trials", default = 1000, type = int, action = "store", help = "how many random trials to do")
    parser.add_argument("--omit_zero", default = False, type = bool, action = "store", help = "is zero a valid value when assigning")

    args = parser.parse_args()
    n_low = args.n_low
    if args.n_high is None:
        n_high = n_low
    l_low = args.l_low
    if args.l_high is None:
        l_high = l_low

    for l in range(l_low,l_high+1):
        for n in range(n_low,n_high+1):
            if args.assign_mode == "random":
                testEvaluations(n,l, "random", args.num_trials, args.omit_zero)
            else:
                testEvaluations(n,l, "bruteforce")

