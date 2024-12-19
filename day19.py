import re
from collections import defaultdict
import sys
import random
import math
import numpy as np
import heapq

from input19 import *

test19="""r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

def canMatch(pattern,i,setIFailed,towels):
    if i == len(pattern):
        return True
    
    # search every prefix
    for towel in towels:
        c = len(towel)
        if i+c not in setIFailed:
            if i+c <= len(pattern) and pattern[i:i+c] == towel:
                if canMatch(pattern, i+c, setIFailed,towels):
                    return True
    
    setIFailed.add(i)

    return False

def day19a(s):

    sTowels,sPatterns = s.split("\n\n")

    towels = set(sTowels.split(", "))
    patterns = list(sPatterns.split('\n'))

    total = 0
    n = -0
    for pattern in patterns:
        setIFailed = set()
        f = canMatch(pattern,0,setIFailed,towels)
        # print(f"{n}/{len(patterns)}: {pattern} {'can' if f else 'can not'} be made")
        if f:
            total += 1
        n += 1

    print(f"total = {total}")


# day19a(test19)
# day19a(input19)

def cMatch(pattern,i,mpICMatch,towels):
    if i == len(pattern):
        return 1
    
    # instead of hash, could proceed from (either) end and fill in array
    if i in mpICMatch:
        return mpICMatch[i]
    
    # search every prefix
    # Could make this much faster by storing in different data structure, e.g. a trie
    # Or check whether each prefix up to max len is in set of towels!
    cm = 0
    for towel in towels: 
        ct = len(towel)
        if i+ct <= len(pattern) and pattern[i:i+ct] == towel:
            cm += cMatch(pattern,i+ct,mpICMatch,towels)
    
    mpICMatch[i] = cm
    return cm

def day19b(s):

    sTowels,sPatterns = s.split("\n\n")

    towels = set(sTowels.split(", "))
    patterns = list(sPatterns.split('\n'))

    total = 0
    for pattern in patterns:
        mpICMatch = {}
        total += cMatch(pattern,0,mpICMatch,towels)

    print(f"total = {total}")


# day19b(test19)
# day19b(input19)

def day19v2(s):
    # better version after having finished with above version

    sTowels,sPatterns = s.split("\n\n")

    towels = set(sTowels.split(", "))
    ctMax = max(map(len, towels)) + 1
    patterns = list(sPatterns.split('\n'))

    possible = 0
    combos = 0
    for pattern in patterns:
        mpCCMatch = [1] # how many combos for first c chars of pattern
        cp = len(pattern)
        for c in range(1,cp+1):
            cm = 0
            for ct in range(1,min(ctMax,c+1)):
                if pattern[c-ct:c] in towels:
                    cm += mpCCMatch[c-ct]
            mpCCMatch.append(cm)
        if mpCCMatch[cp] > 0:
            possible += 1
        combos += mpCCMatch[cp]

    print(f"possible = {possible}, combos = {combos}")

day19v2(input19)
