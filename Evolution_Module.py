import random
from multiprocessing import Process
import Validation

def Multithread_Evaluate(population, classifier, data_set, num_threads):
    split_num = int(len(population)/num_threads)
    start = 0
    end = split_num
    threads = []
    for i in range(num_threads):
        thread = Process(target = Evaluate,args = (population, classifier, data_set[:], start, end))
        threads.append(thread)
        end = end + split_num
        start = end - split_num
        
    if __name__ == "__main__":
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

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

def Mutate(mask, mutation_rate):
    for i in range(len(mask)):
        if random.random() < mutation_rate:
            if mask[i] == 0:
                mask[i] = 1
            else:
                mask[i] = 0
def Two_Point_Crossover(parents):
    children = []
    for i in range(0, len(parents), 2):
        first_cut_index = random.randint(1, 47)
        second_cut_index = random.randint(48, 94)
        child_1 = parents[i][0][:first_cut_index] + parents[i+1][0][first_cut_index:second_cut_index] + parents[i][0][second_cut_index:]
        child_2 = parents[i+1][0][:first_cut_index] + parents[i][0][first_cut_index:second_cut_index] + parents[i+1][0][second_cut_index:]

        children.append([child_1,-1])
        children.append([child_2,-1])
    return children

def Single_Point_Crossover(parents):
    children = []
    for i in range(0,len(parents),2):
        cut_index = random.randint(1, 94)
        child_1 = parents[i][0][:cut_index] + parents[i + 1][0][cut_index:]
        child_2 = parents[i+1][0][:cut_index] + parents[i][0][cut_index:]
        Mutate(child_1, .1)
        Mutate(child_2, .1)
        children.append([child_1,-1])
        children.append([child_2,-1])
    return children

def Replace_Worst_Parents(population, children):
    population.sort(key = lambda x: x[1])
    for i in range(len(children)):
        population[i] = children[i]


def fitness_analytics(population):
    sum = 0
    max_value = 0
    min_value = 1
    for individual in population:
        sum = sum + individual[1]
        if individual[1] > max_value:
            max_value = individual[1]
        if individual[1] < min_value:
            min_value = individual[1]
    return sum/len(population), max_value, min_value

def Feature_Evolution(classifier, data_set, generations=100, population=20, num_children=2, breeding_algorithm="single_point_crossover", mutation_rate=0.1):
    random.seed(123)
    t = 0
    population = [[[round(random.random()) for _ in range(95)], -1] for _ in range(population)]
    Evaluate(population, classifier, data_set)
    with open("GA_Results.csv", "a") as file:
        file.write("Generation,Individual,Fitness\n")
    while t < generations:
        with open("GA_Results.csv", "a") as file:
            for individual in population:
                file.write("{0},{1},{2}\n".format(t, "".join(str(x) for x in individual[0]) ,individual[1]))
        mean_fitness, max_fitness, min_fitness = fitness_analytics(population)
        print("Generation {0} mean accuracy: {1}\n\tmax accuracy: {2}\n\tmin accuracy: {2}\n".format(t, mean_fitness, max_fitness, min_fitness))
        #individuals_to_breed = random.sample(population, num_children)
        individuals_to_breed = sorted(population, key = lambda x: x[1], reverse = True)[:num_children]
        children = Single_Point_Crossover(individuals_to_breed)
        Evaluate(children, classifier, data_set)
        Replace_Worst_Parents(population, children)
        t = t + 1