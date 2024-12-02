import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input1 import *

test1="""3   4
4   3
2   5
1   3
3   9
3   3"""


def day1a(s):
    ls=[]
    rs=[]
    for line in s.split('\n'):
        l,r = map(int, line.split('   '))
        ls.append(l)
        rs.append(r)
    ls.sort()
    rs.sort()
    total = sum(map(lambda tup : abs(tup[0] - tup[1]), zip(ls,rs)))
    print(total)

# day1a(input1)


def day1b(s):
    ls=[]
    rs=[]
    for line in s.split('\n'):
        l,r = map(int, line.split('   '))
        ls.append(l)
        rs.append(r)

    rdict = defaultdict(int)
    for r in rs:
        rdict[r] = rdict[r] + 1

    sim = 0
    for l in ls:
        sim += l * rdict[l]

    print(f"similarity={sim}")

day1b(input1)