from numba import cuda
import sys
from random import randint
import numpy as np
 
n = int(sys.argv[1])
maxNumber = int(sys.argv[2])
set = []
winSet = np.zeros((n,), dtype=np.int32)
combinations = np.zeros((n,), dtype=np.int32)
minn = 0
print("Wylosowany zbior: ")
for i in range(n):
    set.append(randint(1, maxNumber))
    print(set[i], end=' ')
print("")
 
setN = np.asarray(set)
 
@cuda.jit()
def main(winSet, combinations, set, min):
    def difference(combination, set):
        setA = 0
        setB = 0
        for i in range(len(combination)):
            if combination[i] == 0:
                setA += set[i]
            else:
                setB += set[i] 
        return abs(setA-setB)
 
    lenBits = pow(2, n)
    setA = 0
    setB = 0
    for i in range(len(winSet)):
        if winSet[i] == 0:
            x = set[i]
            setA = setA + x
        else:
            setB += set[i] 
    min = abs(setA-setB)
 
    for i in range(lenBits):
        i_n = i
        j = 0
        while i_n != 0:
            if i_n%2 == 0:
                combinations[j] = 0
            else:
                combinations[j] = 1
            i_n //= 2
            j += 1
 
        difff = difference(combinations, set)
        if difff < min:
            min = difff
            winSet = combinations
arr = np.asarray(set)
threadsperblock = 32
blockspergrid = (arr.size + (threadsperblock - 1)) // threadsperblock
 
main[blockspergrid, threadsperblock](winSet, combinations, setN, minn)