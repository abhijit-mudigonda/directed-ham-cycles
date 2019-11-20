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
    print(n, agreements)
    return agreements
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_low", default = 2, type = int, action = "store", help = "smallest K_n to try")
    parser.add_argument("--n_high", default = 11, type = int, action = "store", help = "largest K_n to try")
    parser.add_argument("--min_idx", default = 7, type = int, action = "store", help = "how far back you want to print columns")

    args = parser.parse_args()
 
    agreements_list = []
    print("Intersection lists for each K_n")
    for n in range(args.n_low, args.n_high):
        agreements_list.append(agreementPattern(n))


    #Prints the columns

    print("Columns of the above list, starting at the last nontrivial index and going backwards")
    outs = []
    for i in range(-args.min_idx, -3):
        out = []
        for j in range(-i-3,args.n_high-2):
            out.append(agreements_list[j][i])
        outs.append(out)
    for idx, out in enumerate(reversed(outs)):
        print(idx+1, out)
 


    
