def euclidian_distance(vector1, vector2):
    """Calculates the euclidian distance between two vectors"""
    result = 0
    for x_value, y_value in zip(vector1, vector2):
        result = result + (y_value - x_value)**2
    return result**(1/2)

def load_dataset(filename, split_ratio=0.5):
    test_set = []
    training_set = []
    with open(filename, 'csv'):
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    for x in range(len(dataset)-1):
	        for y in range(4):
	            dataset[x][y] = float(dataset[x][y])
	        if random.random() < split:
	            trainingSet.append(dataset[x])
	        else:
	            testSet.append(dataset[x])
    return (training_set, test_set)