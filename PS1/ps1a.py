###########################
# 6.0002 Problem Set 1a: Space Cows 


import enum
from json import load
from unicodedata import name
from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Questions: Greedy Algorith is optimal, both are but greedy is faster

# Problem 1
def load_cows(filename):
    cows = {}
    cow_data = open(filename, 'r', encoding='utf-8')
    with cow_data:
        for line in cow_data:
            line = line.replace('\n', '')
            array = line.split(',')
            # add cow to dicc, parse number into int
            cows[array[0]] = int(array[1])
    return cows



# Problem 2

# helper function to calculate total weight in transport list
def getTotalWeight(list):
    if(list):
        weight = 0
        for item in list:
            weight = weight + item[1] # cows saved as tupel
        return weight
    else:
        return 0
# helper function to sort cows by weight
def sort(cows: dict):
    sortedList = []
    keys = list(cows.keys())
    for y in range (0, len(cows.keys())):
        biggest = cows[keys[0]]
        biggestName = keys[0]
        for x in range(1, len(keys)):
            if cows[keys[x]] > biggest:
                biggest = cows[keys[x]]
                biggestName = keys[x]
        sortedList.append(biggestName)
        keys.remove(biggestName)   
    return sortedList

# loop over cows and select heaviest cow and check if it still fits, if it does take next one until
# every cow has been considered, then close transport and move on to the next one
def greedy_cow_transport(cows: dict,limit=10):

    transportList = []
    # keep track of created nested lists
    counter = 0
    # copy cws dic to not modify the original
    cowsCopy = cows.copy()
    while(cowsCopy):
        # sort cows by weight
        sorted = sort(cowsCopy)
        for idx,cow in enumerate(sorted):
            if(idx == 0):
                # append cow weight + name in sublist
                transportList.append([(cow, cows[cow])])
                del cowsCopy[cow]
            else:
                # check if transport is not overweight with one more cow
                if(getTotalWeight(transportList[counter]) + cowsCopy[cow]) <= (limit):
                    transportList[counter].append((cow, cows[cow]))
                    del cowsCopy[cow]
        counter += 1
    return transportList

# Problem 3
def brute_force_cow_transport(cowsDict: dict,limit=10):
    # work with names instead of cow weight, otherwiese partition function does not work properly since it is 
    # working with sets and duplicates are removed
    cows = cowsDict.copy()
    startPartition = []
    for cow in list(cows.keys()):
        startPartition.append(cows[cow])
    # keep track of the current best transport list
    bestPartition = [[]]
    first = True
    for partition in get_partitions(cows.keys()):
        valid = True
        # for each possible transport list, check if it is valid
        # loop over each transport in the transport list and check if weight limit is not overexerted
        for item in partition:
            totalWeight = 0
            for cow in item:
                totalWeight = totalWeight + cows[cow]
            if totalWeight > 10:
                valid = False
                break
        if(valid):
            # if possilble list is valid, check if solution is more efficient than current ones
            if(len(bestPartition) > len(partition) or first == True):
                first = False
                bestPartition = partition
    return bestPartition

  
# Problem 4: Compare both algorithms
def testAlogrithm(function, cows: dict):
    start = time.time()
    transportPlan = function(cows)
    stop = time.time()
    timeNeeded = stop - start
    print(f'Time needed: {timeNeeded} \nPlan: {transportPlan}\nNumber of trips needed: {len(transportPlan)}')

def compare_cow_transport_algorithms():
    cowsDic = load_cows('ps1_cow_data.txt')
    print('=============== Brute Force =======================')
    testAlogrithm(brute_force_cow_transport, cowsDic)
    print('=============== Greedy ======================')
    testAlogrithm(greedy_cow_transport, cowsDic)

compare_cow_transport_algorithms()


# Problem 5: Writeup

#1.  What were your results from compare_cow_transport_algorithms? Which algorithm runs faster? Why?
'''
brute force: 0.5 s
greedy: 0.0001 s
=> since the greedy algorith does not consider every possible solution it basically consists out of a
    nested loop which is runs in complexity 
Time complexity
- brute force: O(2^n) (n = number of cows, since we have to consider every possible combination)
- greedy: O(n log (n)) for quick or merge sort O(n^2) for insertion sort 
'''
# TODO : revise time complexity

#2.  Does the greedy algorithm return the optimal solution? Why/why not? 
'''
In this particular case it did not, it only returned a local max, generally speaking we don't know 
how good the returned sulution is.

'''
#3.  Does the brute force algorithm return the optimal solution? Why/why not? 
'''
Yes, since we consider every possible solution and select the best one.
'''