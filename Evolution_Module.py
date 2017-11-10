import random
import Validation


# Evaluation 
def Evaluate(population, classifier, data_set, start=0, end=-1):
    if end == -1:
        end = len(population)
    for i in range(start, end):
        classifier.set_feature_mask(population[i][0])
        result = Validation.leave_one_out_validation(classifier, data_set)
        print("Indiviual: {}".format("".join(str(x) for x in population[i][0])))
        print("\tAccuracy: {}".format(result[0]))
        print("\tMSE: {}".format(result[5]))
        print("\tTrue Positives: {}".format(result[1]))
        print("\tTrue Negatives: {}".format(result[2]))
        print("\tFalse Positives: {}".format(result[3]))
        print("\tFalse Negatives: {}\n".format(result[4]))
        population[i][1] = result[0]

def Evaluate_FeatureMask(population, classifier):
    for i in range(len(population)):
        magnitude = sum(x*x for x in population[i][0])**(1/2)
        normalized_vector = [x/magnitude for x in population[i][0]]
        result = classifier.classify(normalized_vector)
        population[i][1] = result


# Procreation
def Two_Point_Crossover(parents,num_features):
    children = []
    for i in range(0, len(parents), 2):
        first_cut_index = random.randint(1, num_features/2)
        second_cut_index = random.randint((num_features/2) + 1, num_features)
        child_1 = parents[i][0][:first_cut_index] + parents[i+1][0][first_cut_index:second_cut_index] + parents[i][0][second_cut_index:]
        child_2 = parents[i+1][0][:first_cut_index] + parents[i][0][first_cut_index:second_cut_index] + parents[i+1][0][second_cut_index:]

        children.append([child_1,-1])
        children.append([child_2,-1])
    return children

def Single_Point_Crossover(parents,num_features):
    children = []
    for i in range(0,len(parents),2):
        cut_index = random.randint(1, num_features-1)
        child_1 = parents[i][0][:cut_index] + parents[i + 1][0][cut_index:]
        child_2 = parents[i+1][0][:cut_index] + parents[i][0][cut_index:]
        Mutate(child_1, .1)
        Mutate(child_2, .1)
        children.append([child_1,-1])
        children.append([child_2,-1])
    return children

def Uniform_Crossover(parents):
    child = []
    for i in range(len(parents[0][0])):
        parent = random.sample(parents, 1)
        child.append(parent[0][0][i])
    return [[child,-1]]

def Mutate(mask, mutation_rate):
    for i in range(len(mask)):
        if random.random() < mutation_rate:
            if mask[i] == 0:
                mask[i] = 1
            else:
                mask[i] = 0

def BLX(parent1, parent2, m):
    child = []
    for i in range(len(parent1[0])):
        if parent1[0][i] < parent2[0][i]:
            child.append(random.uniform(max(0, parent1[0][i] - m), min(1, parent2[0][i] + m)))
        else:
            child.append(random.uniform(max(0, parent2[0][i] - m), min(1, parent1[0][i] + m)))
    return [child,-1]

# Replacement
def Replace_Worst_Parent(population, child):
    population.sort(key = lambda x: abs(x[1]), reverse = True)
    population[0] = child

def Remove_Worst_Indiviuals(population, num_remove):
    population.sort(key = lambda x: x[1])
    return population[num_remove:]

# Parent Selection
def TournamentSelection(population, k):
    individuals = random.sample(population, k)
    return min(individuals, key = lambda x: abs(x[1]))

# Utility
def fitness_analytics(population):
    sum = 0
    for p in population:
        sum += p[1]
    max_value = max(population, key = lambda x: abs(x[1]))[1]
    min_value = min(population, key = lambda x: abs(x[1]))[1]
    return sum/len(population), max_value, min_value

# GA Algorithms
def Feature_Evolution(classifier, data_set, generations=100, population=20, num_children=2, mutation_rate=0.1, num_features=95):
    random.seed(6)
    t = 0
    population = [[[round(random.random()) for _ in range(num_features)], -1] for _ in range(population)]
    Evaluate_aa(population, classifier, data_set)
    with open("Trials/GA_Results16.csv", "w") as file:
        file.write("Generation,Fitness,Individual\n")
    while t < generations:
        with open("Trials/GA_Results16.csv", "a") as file:
            for individual in population:
                file.write("{0},{2},{1}\n".format(t, "".join(str(x) for x in individual[0]) ,individual[1]))
        mean_fitness, max_fitness, min_fitness = fitness_analytics(population)
        print("Generation {0} mean accuracy: {1}\n\tmax accuracy: {2}\n\tmin accuracy: {3}\n".format(t, mean_fitness, max_fitness, min_fitness))
        individuals_to_breed = random.sample(population, num_children)
       # individuals_to_breed = sorted(population, key = lambda x: x[1], reverse = True)[:num_children]
        children = Uniform_Crossover(individuals_to_breed)
        Evaluate_aa(children, classifier, data_set)
        for child in children:
            population.append(child)
        population = Remove_Worst_Indiviuals(population, len(children))
        t = t + 1

def Feature_Vector_Evolution(classifier, filename, seed, generations=180, population=20, num_children=1, num_features=95):
    random.seed(seed)
    t = 0
    values = [[] for _ in range(96)]
    population = [[[random.random() for _ in range(num_features)], -1] for _ in range(population)]
    Evaluate_FeatureMask(population, classifier)
    with open("Assignment4_Trials/{}.csv".format(filename), "w") as file:
        file.write("Generation,Fitness,Individual\n") 
        for individual in population:
            values[0].append(individual[1])
            for i in range(1,96):
                values[i].append(individual[0][i-1])
            file.write("{0},{2},{1}\n".format(t, ",".join(str(x) for x in individual[0]) ,individual[1]))
    while t < generations:
        mean_fitness, max_fitness, min_fitness = fitness_analytics(population)
        print("Generation {0} mean accuracy: {1}\n\tmax accuracy: {2}\n\tmin accuracy: {3}\n".format(t, mean_fitness, max_fitness, min_fitness))
        parent1 = TournamentSelection(population, 2)
        parent2 = TournamentSelection(population, 2)
        child = BLX(parent1, parent2, 0.0)
        Evaluate_FeatureMask([child], classifier)
        with open("Assignment4_Trials/{}.csv".format(filename), "a") as file:
            file.write("{0},{2},{1}\n".format(t, ",".join(str(x) for x in child[0]) ,child[1]))
        values[0].append(child[1])
        for i in range(1,96):
            values[i].append(child[0][i-1])
        Replace_Worst_Parent(population, child)
        t = t + 1
    means200 = []
    meansfirst100 = []
    meanslast100 = []
    stds200 = []
    stdsfirst100 = []
    stdslast100 = []
    for i in range(96):
        means200.append(sum(values[i])/200)
    for i in range(96):
        meansfirst100.append(sum(values[i][:100])/100)
    for i in range(96):
        meanslast100.append(sum(values[i][100:])/100)
    for i in range(96):
        stds200.append((sum((x - means200[i])**2 for x in values[i])/200)**(1/2))
    for i in range(96):
        stdsfirst100.append((sum((x - meansfirst100[i])**2 for x in values[i][:100])/100)**(1/2))
    for i in range(96):
        stdslast100.append((sum((x - meanslast100[i])**2 for x in values[i][100:])/100)**(1/2))
        
    with open("Assignment4_Trials/MeansAndSigmas.csv".format(filename), "a") as file:
        file.write(",".join(str(x) for x in means200))
        file.write("\n")
        file.write(",".join(str(x) for x in meansfirst100))
        file.write("\n")
        file.write(",".join(str(x) for x in meanslast100))
        file.write("\n")
        file.write(",".join(str(x) for x in stds200))
        file.write("\n")
        file.write(",".join(str(x) for x in stdsfirst100))
        file.write("\n")
        file.write(",".join(str(x) for x in stdslast100))
        file.write("\n\n")