import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input5 import *

def parse(s):
    foundBreak = False
    orders = set()
    updates = []

    for line in s.split('\n'):
        if not foundBreak:
            if len(line) == 0:
                foundBreak = True
            else:
                orders.add(tuple(map(int, line.split('|'))))
        else:
            updates.append(list(map(int, line.split(','))))

    # print(orders)
    # print(updates)

    return orders, updates

def isOrderedCorrectly(update, orders):
    fOk = True
    for i in range(len(update) - 1):
        for j in range(i+1, len(update)): # overkill? Only need to compare pairs?
            if (update[j],update[i]) in orders:
                # print(f"failed {update} because {update[j]}|{update[i]} in orders")
                return False
    return True

def day5a(s):

    orders, updates = parse(s)

    sum = 0
    for update in updates:
        if isOrderedCorrectly(update, orders):
            sum += update[len(update) // 2]
    print(sum)


# day5a(test5)
# day5a(input5)


def day5b(s):

    orders, updates = parse(s)

    sum = 0
    for update in updates:
        if not isOrderedCorrectly(update, orders):
            sortedUpdate = [update[0]]

            # insertion sort

            for page in update[1:]:
                # print(sortedUpdate, page)
                insertAt = len(sortedUpdate)
                for i in range(len(sortedUpdate)):
                    if (page,sortedUpdate[i]) in orders:
                        insertAt = i
                        break
                sortedUpdate.insert(insertAt, page)

            # print(f"old {update} => new {sortedUpdate}")
            assert(isOrderedCorrectly(sortedUpdate, orders))

            sum += sortedUpdate[len(update) // 2]
    print(sum)

# day5b(test5)
day5b(input5)
