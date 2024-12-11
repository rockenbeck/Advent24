import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input11 import *

test11="""125 17"""

def day11a(s):
    a = list(map(int, s.split(" ")))

    # brute force works OK for a while

    for i in range(25):
        aNew = []
        for n in a:
            sn = str(n)
            if n == 0:
                aNew.append(1)
            elif len(sn) % 2 == 0:
                h = len(sn) // 2
                aNew.append(int(sn[:h]))
                aNew.append(int(sn[h:]))
            else:
                aNew.append(n * 2024)
        a = aNew

    print(f"len = {len(a)}")

# day11a(test11)
# day11a(input11)

def lenfromnc(n, c, mpnclen):
    if c == 0:
        return 1
    
    # memoization FTW
    if (n,c) in mpnclen:
        return mpnclen[(n,c)]
    
    sn = str(n)
    if n == 0:
        l = lenfromnc(1, c - 1, mpnclen)
    elif len(sn) % 2 == 0:
        h = len(sn) // 2
        l = lenfromnc(int(sn[:h]), c - 1, mpnclen) + lenfromnc(int(sn[h:]), c - 1, mpnclen)
    else:
        l = lenfromnc(n * 2024, c - 1, mpnclen)
    
    mpnclen[(n,c)] = l # forgot this line the first time. head slap

    return l

def day11b(s):
    a = list(map(int, s.split(" ")))

    mpnclen = {}
    total = 0
    for n in a:
        total += lenfromnc(n, 750, mpnclen) # runs out of stack before 1000

    print(f"total = {total} (hash size {len(mpnclen)})")

# day11b(test11)
day11b(input11)
