#!/usr/bin/python

import argparse
from typing import List, Dict, Tuple, Any
from itertools import permutations
from pyfinite import ffield
import numpy as np

def agreementPattern(n: int) -> List[int]:
    """
        n: The number of vertices in the complete graph in question

        Returns and prints a length (n+1) list of integers whose ith entry is the number
        of Hamiltonian cycles which share i edges with the Hamiltonian cycle
        1 -> 2 -> 3 ... -> n -> 1 in the complete graph K_n


        Hamiltonian cycles are enumerated by enumerating over permutations of n-1 elements. 
    """

    agreements = [0]*(n+1)
    for perm in permutations(list(range(2,n+1))):
        agrees = 0
        for i in range(n-2):
            if perm[i+1]-perm[i] == 1:
                agrees += 1
        if perm[n-2] == n: 
            agrees += 1
        if perm[0] == 2:
            agrees += 1
        agreements[agrees] += 1
    print(agreements)
    return agreements

def testEvaluations(n: int, l: int):
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
    for num in range(K):
        X = np.ndarray((m), dtype = int)
        for i in range(m):
            X[i] = num & q-1
            num = num >> l
        X = np.reshape(X,(n,n))

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
    for n in [4,5,6]:
        testEvaluations(n,1)



        



            


       



       


    
