import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input2 import *

def issafe(an):
    nPrev = None
    ok = True
    inc = None
    for n in an:
        if nPrev != None:
            if inc == None:
                inc = 1 if n > nPrev else -1
            d = (n - nPrev) * inc
            if d < 1 or d > 3:
                ok = False
                break
        nPrev = n

    return ok

def day2a(s):
    count=0
    for line in s.split('\n'):
        if issafe(map(int, line.split(' '))):
            count += 1

    print(count)

# day2a(test2)
# day2a(input2)

def day2b(s):
    count=0
    for line in s.split('\n'):
        an = list(map(int, line.split(' ')));
        if issafe(an):
            count += 1
        else:
            # Brute-force N^2 algorithm. Not so hard to make O(N), if lists were longer

            for i in range(0,len(an)):
                if issafe(an[:i] + an[i+1:]):
                    count += 1
                    break

    print(count)

# day2b(test2)
day2b(input2)
