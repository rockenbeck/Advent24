import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input7 import *

test7="""190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

def parse(s):
    eqs = []

    yMax = 0
    for line in s.split('\n'):
        sm,rands=line.split(": ")
        sm=int(sm)
        rands = list(map(int, rands.split(" ")))
        eqs.append((sm,rands))
    return eqs

def caneq(sm,rands):
    if len(rands) == 1:
        return rands[0] == sm
    
    if caneq(sm-rands[-1], rands[:-1]):
        return True
    if caneq(sm/rands[-1], rands[:-1]):
        return True
    return False
    
def day7a(s):
    eqs = parse(s)

    total = 0
    for sm,rands in eqs:
        if caneq(sm, rands):
            total += sm
    print(total)



# day7a(test7)
# day7a(input7)


def caneqb(sm,rands):
    if sm!=int(sm):
        return False
    sm=int(sm)
    if len(rands) == 1:
        return rands[0] == sm
    
    if caneqb(sm-rands[-1], rands[:-1]):
        return True
    if caneqb(sm/rands[-1], rands[:-1]):
        return True
    
    # bleah; maybe do it as strings most of the time?
    # or "concatenate" via *10, etc?

    sSm = str(sm)
    sRand = str(rands[-1])
    if len(sSm) > len(sRand) and sSm[-len(sRand):] == sRand:
        if caneqb(int(sSm[:-len(sRand)]), rands[:-1]):
            return True
        
    return False
    
def day7b(s):
    eqs = parse(s)

    total = 0
    for sm,rands in eqs:
        if caneqb(sm, rands):
            total += sm
    print(total)

# day7b(test7)
day7b(input7)
