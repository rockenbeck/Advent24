# import re
from collections import defaultdict
# import sys
# import random
# import math
# import numpy as np
import heapq

from input23 import *

test23="""kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

class Comp:
    def __init__(self, name):
        self.name = name
        self.setCompConnect = set()
        self.setCompConnect.add(self)
        self.compGroup = self
        self.valid = True

    def __repr__(self):
        return self.name

    def compRoot(self):
        compRoot = self
        while compRoot.compGroup != compRoot:
            compRoot = compRoot.compGroup

        compT = self
        while compT.compGroup != compRoot:
            compNext = compT.compGroup
            compT.compGroup = compRoot
            compT = compNext

        return compRoot
    
    def connectTo(self, compOther):
        self.setCompConnect.add(compOther)
        compOther.setCompConnect.add(self)

        compRootSelf = self.compRoot()
        compRootOther = compOther.compRoot()
        compRootOther.compGroup = compRootSelf

def day23a(s):

    mpNameComp = {}

    for line in s.split('\n'):
        names = list(line.split('-'))
        for name in names:
            if name not in mpNameComp:
                mpNameComp[name] = Comp(name)
        
        mpNameComp[names[0]].connectTo(mpNameComp[names[1]])
    
    total = 0
    for name0,comp0 in mpNameComp.items():
        for comp1 in comp0.aCompConnect:
            name1 = comp1.name
            if name1 <= name0:
                continue
            for comp2 in comp0.setCompConnect:
                name2 = comp2.name
                if name2 <= name0 or name2 <= name1:
                    continue
                if name0[0] == 't' or name1[0] == 't' or name2[0] == 't':
                    if comp2 in comp1.setCompConnect:
                        print(f"group {name0}, {name1}, {name2} counts")
                        total += 1
    print(f"total = {total}")

# day23a(test23)
# day23a(input23)


def isFullyConnectedSet(comps):
    for comp in comps:
        if not comp.setCompConnect.issuperset(comps):
            return False
    return True

def cBitsSet(n):
    c = 0
    while n > 0:
        c += 1
        n = n & (n - 1)
    return c

def day23b(s):

    mpNameComp = {}

    for line in s.split('\n'):
        names = list(line.split('-'))
        for name in names:
            if name not in mpNameComp:
                mpNameComp[name] = Comp(name)
        
        mpNameComp[names[0]].connectTo(mpNameComp[names[1]])
    
    # sort by increasing length of connections
    # comps = sorted(mpNameComp.values(), key=lambda comp: len(comp.setCompConnect))
    # for comp in comps:
    #     print(f"{comp} connects to {comp.setCompConnect}")
    # 3379 comps in main input, each has exactly 13 connections

    comps = set(mpNameComp.values())

    cConnMax = max(map(lambda comp:len(comp.setCompConnect), comps))
    # print(cConnMax)

    # Since all comps have same number of connections, pre-compute masks to use
    #  ordered by number of bits set in mask, so we can early-exit if we already
    #  have a better solution
    masks = sorted(range(1 << cConnMax), key=lambda n: cBitsSet(n), reverse=True)

    compsBest = []

    for comp in comps:
        assert(len(comp.setCompConnect) == cConnMax) # conveniently true for inputs

        # Try every subset of connections
        # There's probably a faster solution which doesn't try the same subgroups again and again
        # Indeed, the "Clique Problem" is exactly this, with many complicated and
        #  relatively recent algorithms:
        #  https://en.wikipedia.org/wiki/Clique_problem#Finding_maximum_cliques_in_arbitrary_graphs
        # Sounds like the general case is NP-complete, but the fact that the given
        #  graph is sparse and not all that large makes is tractable with more brute-force methods.

        for mask in masks:
            if cBitsSet(mask) <= len(compsBest):
                continue # already have a solution better than any following

            # build set containing connections which match mask
            compsTest = []
            for i,comp in enumerate(comp.setCompConnect):
                if (1 << i) & mask:
                    compsTest.append(comp)
                    # could early exit here if already not complete set, but didn't help much

            if isFullyConnectedSet(compsTest):
                print(f"found fully connected set: {compsTest}")
                compsBest = compsTest

    namesBest = map(lambda comp: comp.name, compsBest)
    password = ','.join(sorted(namesBest))
    print(f"password = {password}")

# day23b(test23)
day23b(input23)
