import re
from collections import defaultdict
import sys
import random
import math
import numpy as np

from input9 import *

test9="""2333133121414131402"""

def parse(s):
    # build lists of files and free areas

    files=[]
    frees=[]

    fFile = True
    iLoc = 0
    for ch in s:
        cLoc = int(ch)
        if fFile:
            files.append((iLoc, cLoc, len(files)))
        else:
            frees.append((iLoc, cLoc))
        iLoc += cLoc
        fFile = not fFile
    cLocTotal = iLoc
    
    return files,frees,cLocTotal

def printFiles(files, cLocTotal):
    # show disk layout represented by files

    disk = "." * cLocTotal
    for iLoc,cLoc,id in files:
        for diLoc in range(cLoc):
            disk = disk[:iLoc+diLoc] + str(id)[0] + disk[iLoc+diLoc+1:]
    print(disk)

def day9a(s):
    files,frees,cLocTotal = parse(s)

    filesExtra = []

    while len(frees) > 0:
        # Fill in first free location with however much of last file will fit
        # Faster algorithm would advance pointer, pulling off files/frees from single list,
        #  and build output as we go, with no need to modify lists at all

        iLocFile, cLocFile,id = files[-1]
        iLocFree, cLocFree = frees[0]
        if iLocFree > iLocFile:
            break
        if cLocFile == cLocFree:
            filesExtra.append((iLocFree, cLocFile, id))
            del(files[-1])
            del(frees[0])
        elif cLocFile > cLocFree:
            filesExtra.append((iLocFree, cLocFree,id))
            files[-1] = (iLocFile, cLocFile - cLocFree,id)
            del(frees[0])
        else:
            assert(cLocFree > cLocFile)
            filesExtra.append((iLocFree, cLocFile,id))
            del(files[-1])
            frees[0] = (iLocFree + cLocFile, cLocFree - cLocFile)

        # printFiles(files + filesExtra, cLocTotal)

    files = files + filesExtra

    # compute final checksum

    check = 0
    for iLoc, cLoc,id in files:
        check += id * (cLoc * (2 * iLoc + cLoc - 1) // 2) # thank you, Carl Friedrich Gauss

    print(check)

# day9a(test9)
# day9a(input9)


def day9b(s):
    files,frees,cLocTotal = parse(s)
    
    # move files down one at a time

    for iFile in range(len(files) - 1, -1, -1):
        iLocFile, cLocFile, id = files[iFile]
        # put it in first free gap of sufficient size
        for iFree in range(len(frees)):
            iLocFree, cLocFree = frees[iFree]
            if iLocFree > iLocFile:
                break
            if cLocFile == cLocFree:
                files[iFile] = (iLocFree, cLocFile, id)
                del(frees[iFree])
                break
            elif (cLocFree > cLocFile):
                files[iFile] = (iLocFree, cLocFile, id)
                frees[iFree] = (iLocFree + cLocFile, cLocFree - cLocFile)
                break

        # printFiles(files, cLocTotal)

    # compute final checksum

    check = 0
    for iLoc,cLoc,id in files:
        check += id * (cLoc * (2 * iLoc + cLoc - 1) // 2) # thank you, Carl Friedrich Gauss

    print(check)

# day9b(test9)
day9b(input9)
