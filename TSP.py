import math
import pandas as pd
import string
import random

strings = string.ascii_lowercase
sampleOfNumber = 0
positions = [[2,7],[6,8],[3,3],[9,0],[15,6],[4,7],[3,8],[5,7],[16,7],[5,2],[7,5],[4,7],[46,32],[36,7]]

def list_chunk(lst,n):
    return [lst[i:i+n]for i in range(0,len(lst),n)]

def pointToPointDistance(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

def createData (array):
    usePositions = len(array)
    temp = []
    x = []
    y = []

    for i in range(len(array)):
        x.append(array[i][0])
        y.append(array[i][1])

    for l in range(len(array)):
        for j in range(len(array)):
            temp.append(pointToPointDistance(x[l], y[l], x[j], y[j]))

    result = (list_chunk(temp,len(array)))
    result.insert(0, usePositions)

    return result

def createPandas(positions):
    global sampleOfNumber
    global strings
    data = createData(positions)
    sampleOfNumber = data[0]
    strings = strings[:sampleOfNumber]
    return pd.DataFrame(data[1:])

table = createPandas(positions)

def createGenes():
    result = random.sample(strings,k=sampleOfNumber)
    return result

def createPopulation(size):
    population = []
    for i in range(size):
        population.append(createGenes())
    return population


def fitness(gene):
    temp = []
    result = 0
    for Gi in range(len(gene)):
        temp.append(list(strings).index(gene[Gi]))

    for gj in range(len(gene)-1):
        result += table[temp[gj]][temp[gj+1]]
    return result

def performace(population):
    performaceList = []
    for pi in population:
        temp = fitness(pi)
        performaceList.append([pi,temp])
    populationSorted = sorted(performaceList, key=lambda x:x[1])
    return populationSorted

def selectSurvivors(populationSorted,bestSample,luckyFew):
    nextGeneration = []
    for si in range(bestSample):
        nextGeneration.append(populationSorted[si][0])

    luckySurvivors = random.sample(populationSorted,luckyFew)
    for si in luckySurvivors:
        nextGeneration.append(si[0])

    if len(nextGeneration)<bestSample+luckyFew:
        nextGeneration.append(createGenes())

    random.shuffle(nextGeneration)
    return nextGeneration

def createChild(individual1,individual2):
    child = ''
    temp = []
    temp2 = list(strings)
    if individual1 == individual2:
        return individual1

    for i in range(len(individual1)):
        if (int(random.random()*100)<50):
            child += individual1[i]
        else:
            child += individual2[i]

    for value in child:
        if value not in temp:
            temp.append(value)
    child = temp
    temp2 = set(temp2)
    temp3 = set(child)
    temp = list(temp2-temp3)

    if len(child)<len(individual1):
        for j in range(len(individual1)-len(child)):
            child += random.choice(temp)
    return child

def createChildren(parents,n_child):
    nextPopulation = []

    for i in range(int(len(parents)/2)):
        for j in range(n_child):
            nextPopulation.append(createChild(parents[i],parents[len(parents)-1-i]))

    return nextPopulation

def mutateGene(Gene):
    word = list(Gene)

    idx1 = int(random.random()*len(Gene))
    idx2 = int(random.random()*len(Gene))
    word[idx1],word[idx2] = word[idx2],word[idx1]

    return list(word)

def createMutation(population,chanceOfMutate):
    for i in range(len(population)):
        if random.random()*100<chanceOfMutate:
            population[i] = mutateGene(population[i])
    return population



pop = createPopulation(100)
for g in range(30000):
    pop_sorted = performace(pop)
    survivors = selectSurvivors(pop_sorted,bestSample=20,luckyFew=20)
    children = createChildren(survivors,5)
    newGeneration = createMutation(children,10)
    pop = newGeneration

    print('===== %sth Generation =====' % (g + 1))
    print((pop_sorted[0]))

