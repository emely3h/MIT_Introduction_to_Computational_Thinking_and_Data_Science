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
            cows[array[0]] = (array[1])
    return cows

cowsDic = {'Maggie': 3, 'Herman': 7, 'Britta':3, 'Hans':2, 'Oreo': 6, 'Moo Moo': 1, 'Millie': 5, 'Florence': 4, 'Henrietta': 2} #load_cows('ps1_cow_data.txt')

# Problem 2

def getTotalWeight(list):
    if(list):
        weight = 0
        for item in list:
            weight = weight + item
        return weight
    else:
        return 0

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


def greedy_cow_transport(cows: dict,limit=10):
    weightList = []
    nameList = []
    counter = 0
    cowsCopy = cows
    while(cowsCopy):
        sorted = sort(cowsCopy)
        for idx,cow in enumerate(sorted):
            if(idx == 0):
                weightList.append([cowsCopy[cow]])
                nameList.append([cow])
                del cowsCopy[cow]
            else:
                if(getTotalWeight(weightList[counter]) + cowsCopy[cow]) < (limit+1):
                    weightList[counter].append(cowsCopy[cow])
                    nameList[counter].append(cow)
                    del cowsCopy[cow]
        counter += 1
    return weightList


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    # partition deletes dublicates

    startPartition = []
    for cow in list(cows.keys()):
        startPartition.append(cows[cow])
    numberOfTrips = 0
    bestPartition = [[]]
    first = True
    for partition in get_partitions(startPartition):
        valid = True
        for item in partition:
            totalWeight = 0
            for cow in item:
                totalWeight = totalWeight + cow
            if totalWeight > 10:
                valid = False
                #  for better efficiency break out of while loop
        if(valid):
            if(numberOfTrips > len(partition) or first == True):
                first = False
                numberOfTrips = len(partition)
                bestPartition = partition

    print("asdf")
    return bestPartition
    

  
# Problem 4

def testAlogrithm(function):
    start = time.time()
    transportPlan = function(cowsDic)
    stop = time.time()
    timeNeeded = stop - start
    print(f'Time needed: {timeNeeded} \nPlan: {transportPlan}\nNumber of trips needed: {len(transportPlan)}')

def compare_cow_transport_algorithms():
    
    testAlogrithm(brute_force_cow_transport)
    testAlogrithm(greedy_cow_transport)

compare_cow_transport_algorithms()