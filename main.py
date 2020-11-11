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

def genetic_algo(weapon,success_probabilities, threat_coeff):
    pass
def WTA(weapons,success_probabilities, threat_coeff):
    pass

#print(init(2, 5))
print(mutation(.5,init(2, 5)))