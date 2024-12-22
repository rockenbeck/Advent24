import re
from collections import defaultdict
import sys
import random
import math
import numpy as np
import heapq

from input22 import *

test22="""1
10
100
2024"""

def mix(a,b):
    return a ^ b

def prune(n):
    return n % 16777216

def day22a(s):

    c = 2000

    total = 0
    for start in map(int, s.split('\n')):
        n = start
        for i in range(c):
            n = prune(mix(n, n * 64))
            n = prune(mix(n, n // 32))
            n = prune(mix(n, n * 2048))
        # print(f"{start}: {n}")
        total += n
    print(f"total = {total}")
            

# day22a(test22)
# day22a(input22)

test22b="""1
2
3
2024"""

def day22b(s):

    c = 2000

    # this works (and solved the problem), but is pretty slow -- took a couple of minutes

    ampHistPrice = []
    setHist = set()

    for start in map(int, s.split('\n')):
        mpHistPrice = defaultdict(lambda:0)
        ampHistPrice.append(mpHistPrice)
        hist = ()
        n = start
        pricePrev = n % 10
        for i in range(c):
            n = prune(mix(n, n * 64))
            n = prune(mix(n, n // 32))
            n = prune(mix(n, n * 2048))
            price = n % 10
            t = (price - pricePrev,)
            if len(hist) == 4:
                hist = hist[1:4] + t
            else:
                hist += t
            if len(hist) == 4:
                if hist not in mpHistPrice:
                    mpHistPrice[hist] = price
                    setHist.add(hist)
            pricePrev = price

    bestTotal = 0
    bestHist = None

    for hist in setHist:
        if hist==(-2,1,-1,3):
            print("")
        total = 0
        for mpHistPrice in ampHistPrice:
            total += mpHistPrice[hist]
        if total > bestTotal:
            bestTotal = total
            bestHist = hist

    print(f"hist = {bestHist} total = {bestTotal}")

def day22bv2(s):

    c = 2000

    # considerably faster than v1, by adding in totals as we go
    
    mpHistPriceTotal = defaultdict(lambda:0)

    for start in map(int, s.split('\n')):
        setHist = set()
        hist = ()
        n = start
        pricePrev = n % 10
        for i in range(c):
            n = prune(mix(n, n * 64))
            n = prune(mix(n, n // 32))
            n = prune(mix(n, n * 2048))
            price = n % 10
            t = (price - pricePrev,)
            if len(hist) == 4:
                hist = hist[1:4] + t
            else:
                hist += t
            if len(hist) == 4:
                if hist not in setHist:
                    setHist.add(hist)
                    mpHistPriceTotal[hist] = mpHistPriceTotal[hist] + price
                    
            pricePrev = price

    bestTotal = 0
    bestHist = None

    for hist,total in mpHistPriceTotal.items():
        if total > bestTotal:
            bestTotal = total
            bestHist = hist

    print(f"hist = {bestHist} total = {bestTotal}")

# day22b(test22b)
day22bv2(input22)
