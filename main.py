import random

population_num = 10
bit_filp = 0.2
iteration_num = 100
selection_num = 2


def checkIfDuplicates(listOfElems):
    res = []
    sum = 0
    for elem in listOfElems:
        if elem not in res:
            res.append(elem)
            sum += 1

    return sum


def init(population_num, weapon_num, used_weapons):
    population = []
    for i in range(0, population_num):
        chromosome = []
        for j in range(0, weapon_num):
            r = random.randrange(0, 2) * used_weapons[j]
            chromosome.append(r)
        population.append(chromosome)
    return population


def check(population, success_prop, target_coeff, used_weapons):
    result_population = []
    invaild = 0
    chromLen = 0
    for i in range(0, len(population)):
        propSum = 0
        for j in range(0, len(population[i])):
            chromLen = len(population[i])
            if (population[i][j] == 1):
                propSum += target_coeff * success_prop[j]
        propSum = target_coeff  - propSum
        if propSum >= 0:
            result_population.append(population[i])
        else:
            invaild += 1
    new = init(invaild, chromLen, used_weapons)
    if invaild > 0:
        result_population = result_population + check(new, success_prop, target_coeff, used_weapons)
    return result_population


def fitness_and_selection(population, threat_coeff, success_probabilities, selectionNumber):
    if selectionNumber % 2 != 0:
        print("Selection Must be EVEN")
        return None
    fitness = []
    commulativeFitness = []
    selection = []
    for i in range(0, len(population)):
        fitnessProcess = 0
        for j in range(0, len(population[i])):
            fitnessProcess += population[i][j] * threat_coeff * success_probabilities[j]
        if fitnessProcess == 0:
            fitness.append(0)
        else:
            fitness.append(1 / fitnessProcess)
    commulativeFitness.append(fitness[0])
    for k in range(1, len(fitness)):
        addProccess = commulativeFitness[k - 1] + fitness[k]
        commulativeFitness.append(addProccess)
    prob_num = checkIfDuplicates(population)
    if prob_num < selectionNumber:
        selectionNumber = prob_num // selectionNumber
    while (len(selection) < selectionNumber):
        # print(0)
        randomNumber = random.uniform(0, commulativeFitness[len(commulativeFitness) - 1])
        for m in range(0, len(commulativeFitness)):
            if randomNumber < commulativeFitness[m]:
                if population[m] in selection:
                    continue
                else:
                    selection.append(population[m])
                    break
        selectionNumber -= 2
    return selection


def crossover(selection):
    crossOver = []
    for i in range(0, len(selection) - 1, 2):
        tempArray1 = []
        tempArray2 = []
        randomNumber = random.randrange(0, (len(selection[i]) - 1))
        # print("random: ", randomNumber)
        if (randomNumber == 0):
            crossOver.append(selection[i])
            crossOver.append(selection[i + 1])
            continue
        for j in range(0, randomNumber):
            tempArray1.append(selection[i][j])
            tempArray2.append(selection[i + 1][j])
        for k in range(randomNumber, len(selection[i])):
            tempArray1.append(selection[i + 1][k])
            tempArray2.append(selection[i][k])
        crossOver.append(tempArray1)
        crossOver.append(tempArray2)
    return crossOver


def mutation(bit_filp, crossover, used_weapons):
    for i in range(0, len(crossover)):
        for j in range(0, len(crossover[i])):
            r = random.uniform(0, 1)
            if (r <= bit_filp):
                crossover[i][j] = abs(crossover[i][j] - 1) * used_weapons[j]
    return crossover


def replacement(population, mutation, success_prop):
    # success_prop [.3,.3,.5,.2,.2]
    new_gen = []
    mProp = []
    for x in range(0, len(mutation)):
        mSum = 0
        for y in range(0, len(mutation[x])):
            mSum += mutation[x][y] * success_prop[y]
        mProp.append(mSum)
    for i in range(0, len(population)):
        pSum = 0
        for j in range(0, len(population[i])):
            pSum += population[i][j] * success_prop[j]
        flag = False
        for x in range(0, len(mProp)):
            if mProp[x] > pSum:
                new_gen.append(mutation[x])
                flag = True
                break
        if flag == False:
            new_gen.append(population[i])

    return new_gen


def select_the_fittest(population, target_coeff, success_probabilitie):
    max = 0
    index = 0
    assigned_weapons = population[0]
    for i in range(0, len(population)):
        sum_prop = 0
        for j in range(0, len(population[i])):
            sum_prop += population[i][j] * target_coeff * success_probabilitie[j]
        if sum_prop > max:
            max = sum_prop
            assigned_weapons = population[i]
    return assigned_weapons


def genetic_algo(weapons_types_num, weapon_num_for_type, weapons, target_num, target_coeffs, success_probabilities,
                 used_weapons):
    population = init(population_num, len(weapons), used_weapons)
    print("population: ", population)
    success_probabilitie = []
    for j in range(0, weapons_types_num):
        for k in range(0, weapon_num_for_type[j]):
            success_probabilitie.append(success_probabilities[j][target_num])
    print(success_probabilitie, target_coeffs[target_num])
    for i in range(0, iteration_num):
        population = check(population, success_probabilitie, target_coeffs[target_num], used_weapons)
        # print("population after check: ", population)
        selections = fitness_and_selection(population, target_coeffs[target_num], success_probabilitie, selection_num)
        # print("selection: ", selections)
        crossover_out = crossover(selections)
        # print("selection after crossover: ", crossover_out)
        mutation_out = mutation(bit_filp, crossover_out, used_weapons)
        # print("selection after mutation: ", mutation_out)
        population = replacement(population, mutation_out, success_probabilitie)
    print("final population: ", population)
    assigned_weapons = select_the_fittest(population, target_coeffs[target_num], success_probabilitie)
    return assigned_weapons,success_probabilitie


def WTA_input():
    weapons = []
    weapons_types_num = 0
    weapon_num_for_type = []
    print("Enter the weapon types and the number of instances of each type: (Enter“x” when you’re done)")
    while True:
        weapon_name = str(input())
        if (weapon_name == "x"):
            break
        weapon_num = int(input())
        for i in range(0, weapon_num):
            weapons.append(weapon_name + str(i + 1))
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
    return weapons_types_num, weapon_num_for_type, weapons, target_num, target_coeffs, success_probabilities


def WTA():
    # weapons_types_num,weapon_num_for_type, weapons, target_num, target_coeffs, success_probabilities= WTA_input()
    # test
    weapons_types_num, weapon_num_for_type, weapons, target_num, target_coeffs, success_probabilities = 3, [2, 1, 2], [
        'tank1', 'tank2', 'air1', 'grenade1', 'grenade2'], 3, [16, 5, 10], [[0.3, 0.6, 0.5], [0.4, 0.5, 0.4],
                                                                            [0.1, 0.2, 0.2]]
    print(weapons_types_num, weapon_num_for_type, weapons, target_num, target_coeffs, success_probabilities)
    target_id = []
    for i in range(0, target_num):
        target_id.append(i)
    target_id = [target_id for _, target_id in sorted(zip(target_coeffs, target_id), reverse=True)]
    targets = []
    used_weapons = []

    for j in range(0, len(weapons)):
        used_weapons.append(1)
    # print(used_weapons)
    target_success_probabilitie=[]
    for i in range(0, target_num):
        res,success_probabilitie = genetic_algo(weapons_types_num, weapon_num_for_type, weapons, target_id[i], target_coeffs,
                           success_probabilities, used_weapons)
        targets.append(res)
        target_success_probabilitie.append(success_probabilitie)
        # print(res)
        for j in range(0, len(res)):
            if used_weapons[j] == 1:
                used_weapons[j] = 1 - res[j]
        # print(used_weapons)
        if sum(used_weapons) == 0:
            break
    print("the final result is:", targets)
    return final_result(targets, weapons, target_coeffs, target_success_probabilitie)


# Tank #1 is assigned to target #1,
def final_result(targets, weapons, target_coeffs, target_success_probabilitie):
    print(target_success_probabilitie)
    expected_total_threat = 0
    for i in range(0, len(targets)):
        expected_threat_of_target =0
        for j in range(0, len(targets[i])):
            if targets[i][j] == 1:
                print(weapons[j], "is assigned to target", i+1)
                print(target_success_probabilitie[i][j] , target_coeffs[i])
                expected_threat_of_target += target_success_probabilitie[i][j] * target_coeffs[i]
        expected_total_threat += target_coeffs[i] - expected_threat_of_target
    return expected_total_threat

print("the final result is:", WTA())
