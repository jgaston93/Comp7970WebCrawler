import math
import statistics

def euclidian_distance(vector1, vector2, vector_mask=None):
    """Calculates the euclidian distance between two vectors"""
    if vector_mask == None:
        vector_mask = [1 for _ in range(len(vector1))]
    if len(vector1) != len(vector2):
        raise ValueError("Vector sizes don't match")
    if len(vector1) != len(vector_mask):
        raise ValueError("Feature mask size doesn't match")
    result = 0
    for x_value, y_value, mask in zip(vector1, vector2, vector_mask):
        if mask == 1:
            result = result + ((y_value - x_value)**2)
    return result**(1/2)

def load_dataset(file_name):
    dataset = []
    with open(file_name, "r") as data_file:
        for line in data_file:
            data_values = line.rstrip().split(" ")
            label = float(data_values[1])
            temp = [float(x) for x in data_values[2:]]
            instance = tuple(temp)
            magnitude_of_vector = math.sqrt(sum(x*x for x in temp))
            if magnitude_of_vector > 0:
                instance = tuple([x/magnitude_of_vector for x in temp])
            dataset.append((instance, label))
    
    print("num features: {}\n".format(len(dataset[0][0])))
    return dataset


def mean(values):
    return sum(values) / float(len(values))

def std_deviation(values):
    if len(values) < 2:
        return 0
    return statistics.stdev(values)