#!/usr/bin/python

import argparse
from typing import List, Dict, Tuple, Any
from itertools import permutations
from pyfinite import ffield
import numpy as np

def agreementPattern(n: int) -> List[int]:
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
    """
    m = n**2
    q = 2**l
    K = q**m
    F = ffield.FField(l)

    zero_count = 0
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
    print("When n = ", n, "and l = ", l, "the fraction of zeros was: ", float(zero_count)/K)

if __name__ == "__main__":
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_vtx", required = True, type = int, action = "store", help = "number of vertices of the complete graph in question")
    parser.add_argument("--field_exponent", required = True, type = int, action = "store", help = "power of 2 whose field you want to use")


    args = parser.parse_args()
    n = args.num_vtx
    l = args.field_exponent
    """
    for n in [4,5,6]:
        for l in [1]:
            testEvaluations(n,l)



        



            


       



       


    
