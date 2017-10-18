import random
import Validation

def Evaluate(population, classifier, data_set):
    for individual in population:
        classifier.set_feature_mask(individual[0])
        result = Validation.leave_one_out_validation(classifier, data_set)
        print("Indiviual: {}".format("".join(str(x) for x in individual[0])))
        print("\tAccuracy: {}".format(result[0]))
        print("\tMSE: {}".format(result[5]))
        print("\tTrue Positives: {}".format(result[1]))
        print("\tTrue Negatives: {}".format(result[2]))
        print("\tFalse Positives: {}".format(result[3]))
        print("\tFalse Negatives: {}\n".format(result[4]))
        individual[1] = result[0]
    return result

def Mutate(mask, mutation_rate):
    for bit in mask:
        if random.random() < mutation_rate:
            if mask == 0:
                mask = 1
            else:
                mask = 0
def Two_Point_Crossover(parent_1, parent_2):
    first_cut_index = random.randint(1, 47)
    second_cut_index = random.randint(48, 94)
    child_1 = parent_1[:first_cut_index] + parent_2[first_cut_index:second_cut_index] + parent_1[second_cut_index:]
    child_2 = parent_2[:first_cut_index] + parent_1[first_cut_index:second_cut_index] + parent_2[second_cut_index:]
    Mutate(child_1, .1)
    Mutate(child_2, .1)
    return [[child_1, -1], [child_2, -1]]

def Single_Point_Crossover(parent_1, parent_2):
    print("Parent 1: {}".format("".join(str(x) for x in parent_1)))
    print("Parent 2: {}".format("".join(str(x) for x in parent_2)))
    cut_index = random.randint(1, 94)
    child_1 = parent_1[:cut_index] + parent_2[cut_index:]
    child_2 = parent_2[:cut_index] + parent_1[cut_index:]
    Mutate(child_1, .1)
    Mutate(child_2, .1)
    print("Child 1: {} + {}".format("".join(str(x) for x in parent_1[:cut_index]), "".join(str(x) for x in parent_2[cut_index:])))
    print("Child 2: {} + {}\n".format("".join(str(x) for x in parent_2[:cut_index]), "".join(str(x) for x in parent_1[cut_index:])))
    return [[child_1, -1], [child_2, -1]]

def Replace_Worst_Parents(population, children):
    parent_1_index = -1
    parent_1_fitness = 0
    parent_2_index = -1
    parent_2_fitness = 0
    current_index = 0
    for individual in population:
        if individual[1] < parent_1_fitness:
            parent_2_index = parent_1_index
            parent_2_fitness = parent_1_fitness
            parent_1_index = current_index
            parent_1_fitness = individual[1]
        elif individual[1] < parent_2_fitness and current_index != parent_1_index:
            parent_2_index = current_index
            parent_2_fitness = individual[1]
        current_index = current_index + 1
    population[parent_1_index] = children[0]
    population[parent_2_index] = children[1]


def calc_generation_mean_fitness(population):
    sum = 0
    for individual in population:
        sum = sum + individual[1]
    return sum/len(population)

def Feature_Evolution(classifier, data_set):
    random.seed(123)
    t = 0
    population = [[[round(random.random()) for _ in range(95)], -1] for _ in range(10)]
    Evaluate(population, classifier, data_set)
    with open("GA_Results.csv", "a") as file:
        file.write("Generation,Individual,Fitness\n")
    while t < 100:
        with open("GA_Results.csv", "a") as file:
            for individual in population:
                file.write("{0},{1},{2}\n".format(t, "".join(str(x) for x in individual[0]) ,individual[1]))
        mean_fitness = calc_generation_mean_fitness(population)
        print("Generation {0} mean accuracy: {1}\n".format(t, mean_fitness))
        individuals_to_breed = random.sample(population, 2)
        children = Single_Point_Crossover(individuals_to_breed[0][0], individuals_to_breed[1][0])
        Evaluate(children, classifier, data_set)
        Replace_Worst_Parents(population, children)
        t = t + 1