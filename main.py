import random
import numpy as np

tank1 = []
def init(population_num, weapon_num):
    population = []
    for i in range(0, population_num):
        chromosome = []
        for j in range(0, weapon_num):
            r = random.randrange(0, 2)
            chromosome.append(r)
        population.append(chromosome)
    return population
def check(population):
    pass
def fitness_and_selection(population,threat_coeff, success_probabilities):
    pass

def crossover(selection):

    pass
def mutation(bit_filp,crossover):

    for i in range(0,len(crossover)):
        for j in range (0,len(crossover[i])):
            r= random.uniform(0, 1)
            if(r>bit_filp):
                crossover[i][j]=abs(crossover[i][j]-1)
    return crossover
def replacement(population,mutation):
    pass

def genetic_algo(weapons,success_probabilities, threat_coeff):
    population_num=7
    bit_filp=0.5
    iteration_num=50
    population=init(7,population_num,len(weapons))
    for i in range(0,iteration_num):
        selections=fitness_and_selection(population,threat_coeff,success_probabilities)
        crossover_out=crossover(selections)
        mutation_out=mutation(bit_filp,crossover_out)
        population=replacement(population,mutation_out)
    return population
def WTA_input():
    weapons = []
    weapons_types_num = 0
    print("Enter the weapon types and the number of instances of each type: (Enter“x” when you’re done)")
    while True:
        weapon_name = str(input())
        if (weapon_name == "x"):
            break
        weapon_num = int(input())
        for i in range(0, weapon_num):
            weapons.append(weapon_name + str(i + 1))
        weapons_types_num += 1
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

    return weapons_types_num,weapons,target_num,target_coeffs,success_probabilities
def WTA():
    weapons_types_num, weapons, target_num, target_coeffs, success_probabilities= WTA_input()
    print(weapons)
    print(target_coeffs)
    print(success_probabilities)

WTA()
