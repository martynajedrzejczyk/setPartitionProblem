import sys
from random import randint

def toBinary(n, lenBits):
    binary = format(n, 'b')
    binary = binary.zfill(lenBits)
    return binary

def difference(combination, set):
    setA = 0
    setB = 0
    for i in range(len(combination)):
        if combination[i] == "0":
            setA += set[i]
        else:
            setB += set[i] 
    return abs(setA-setB)

def partition():
    n = int(sys.argv[1])
    maxNumber = int(sys.argv[2])
    lenBits = pow(2, n)

    set = []
    for i in range(n):
        set.append(randint(1, maxNumber))

    winSet = toBinary(0, n)
    min = difference(winSet, set)

    for i in range(lenBits):
        combinations = toBinary(i, n)
        difff = difference(combinations, set)
        if difff < min:
            min = difff
            winSet = combinations
partition()