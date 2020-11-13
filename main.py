import random
import numpy as np
#test for replacment & check


def init(population_num, weapon_num):
    population = []
    for i in range(0, population_num):
        chromosome = []
        for j in range(0, weapon_num):
            r = random.randrange(0, 2)
            chromosome.append(r)
        population.append(chromosome)
    return population
def check(population , success_prop):
    result_population=[]
    invaild=0
    chromLen=0
    for i in range(0,len(population)):
        propSum = 0
        for j in range (0,len(population[i])):
            chromLen = len(population[i])
            if(population[i][j] == 1):
                propSum += success_prop[j]
        if propSum <= 1:
            result_population.append(population[i])
        else:
            invaild +=1
    new = init(invaild,chromLen)
    if invaild > 0:
        result_population = result_population + check(new,success_prop)
    return result_population
def fitness_and_selection(population,threat_coeff, success_probabilities,selectionNumber):
    if selectionNumber %2 != 0:
        print("Selection Must be EVEN")
        pass
    fitness = []
    commulativeFitness = []
    selection = []
    for i in range(0,len(population)):
        fitnessProcess = 0
        for j in range(0,len(population[i])):
            fitnessProcess += population[i][j] * threat_coeff * success_probabilities[j]
        if fitnessProcess==0:
            fitness.append(0)
        else:
            fitness.append(1 / fitnessProcess)
    commulativeFitness.append(fitness[0])
    for k in range(1,len(fitness)):
        addProccess = commulativeFitness[k - 1] + fitness[k]
        commulativeFitness.append(addProccess)
    for h in range(0, selectionNumber):
        rangeEnd = len(commulativeFitness) - 1
        randomNumber = random.uniform(0, commulativeFitness[rangeEnd])
        for m in range(0, len(commulativeFitness)):
            if randomNumber < commulativeFitness[m]:
                selection.append(population[m])
                break
    return selection

def crossover(selection):
    crossOver = []
    tempArray1 = []
    tempArray2 = []
    for i in range(0,len(selection)-1):
        randomNumber = random.randrange(0,(len(selection[i])-1))
        if(randomNumber == 0):
            crossOver.append(selection[i])
            crossOver.append(selection[i+1])
            i = i + 2
            continue
        #print(randomNumber)
        for j in range (0,randomNumber):
            tempArray1.append(selection[i][j])
            tempArray2.append(selection[i+1][j])
        for k in range (randomNumber, len(selection[i])):
            tempArray1.append(selection[i+1][k])
            tempArray2.append(selection[i][k])
        i = i + 2
        crossOver.append(tempArray1)
        crossOver.append(tempArray2)
    return crossOver
def mutation(bit_filp,crossover):

    for i in range(0,len(crossover)):
        for j in range (0,len(crossover[i])):
            r= random.uniform(0, 1)
            if(r>bit_filp):
                crossover[i][j]=abs(crossover[i][j]-1)
    return crossover
def replacement(population, mutation, success_prop):
    #success_prop [.3,.3,.5,.2,.2]
    new_gen = []
    mProp= []
    for x in range(0, len(mutation)):
        mSum=0
        for y in range(0, len(mutation[x])):
            mSum += mutation[x][y] * success_prop[y]
        mProp.append(mSum)
    for i in range(0, len(population)):
        pSum = 0
        for j in range(0, len(population[i])):
            pSum +=population[i][j] * success_prop[j]
        flag=False
        for x in range(0,len(mProp)):
            if mProp[x] > pSum:
                new_gen.append(mutation[x])
                flag=True
                break
        if flag ==False:
              new_gen.append(population[i])

    return new_gen

def genetic_algo(weapons_types_num,weapon_num_for_type, weapons, target_num, target_coeffs, success_probabilities):
    population_num=7
    bit_filp=0.5
    iteration_num=50
    selection_num=2
    population=init(population_num,len(weapons))
    print(population)
    for i in range(0,iteration_num):

        success_probabilitie=[]
        for j in range(0,weapons_types_num):
            for k in range (0,weapon_num_for_type[j]):
                success_probabilitie.append(success_probabilities[j][target_num])

        #print(success_probabilitie,target_coeffs[target_num])
        population = check(population,success_probabilitie)
        selections=fitness_and_selection(population,target_coeffs[target_num],success_probabilitie,selection_num)
        crossover_out=crossover(selections)
        mutation_out=mutation(bit_filp,crossover_out)
        population=replacement(population,mutation_out,success_probabilitie)
    print(population)
    return population
def WTA_input():
    weapons = []
    weapons_types_num = 0
    weapon_num_for_type=[]
    print("Enter the weapon types and the number of instances of each type: (Enter“x” when you’re done)")
    while True:
        weapon_name = str(input())
        if (weapon_name == "x"):
            break
        weapon_num = int(input())
        for i in range(0, weapon_num):
            weapons.append(weapon_name+str(i+1))
        weapons_types_num += 1
        weapon_num_for_type.append(weapon_num)
    print("Enter the number of targets:")
    target_num = int(input())
    print("Enter the threat coefficient of each target:")
    target_coeffs = []
    for i in range(0, target_num):
        t_coeff = int(input())
        target_coeffs.append(t_coeff)
    print("Enter the weapons’ success probabilities matrix:")
    success_probabilities = []
    for i in range(0, weapons_types_num):
        success_probabilitie = []
        for j in range(0, target_num):
            s_p = float(input())
            success_probabilitie.append(s_p)
        success_probabilities.append(success_probabilitie)
    return weapons_types_num,weapon_num_for_type,weapons,target_num,target_coeffs,success_probabilities
def WTA():
    #weapons_types_num,weapon_num_for_type, weapons, target_num, target_coeffs, success_probabilities= WTA_input()
    #test
    weapons_types_num,weapon_num_for_type, weapons, target_num, target_coeffs, success_probabilities=3,[2, 1, 2],['tank1', 'tank2', 'air1', 'grenade1', 'grenade2'], 3, [16, 5, 10], [[0.3, 0.6, 0.5], [0.4, 0.5, 0.4], [0.1, 0.2, 0.2]]
    print(weapons_types_num,weapon_num_for_type, weapons, target_num, target_coeffs, success_probabilities)
    for i in range(0,target_num):
        res=genetic_algo(weapons_types_num,weapon_num_for_type, weapons, i, target_coeffs, success_probabilities)
        break
WTA()
