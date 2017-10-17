def euclidian_distance(vector1, vector2, vector_mask=[1 for _ in range(95)]):
    """Calculates the euclidian distance between two vectors"""
    result = 0
    for x_value, y_value, mask in zip(vector1, vector2, vector_mask):
        if mask == 1:
            result = result + ((y_value - x_value)**2)
    return result**(1/2)

def load_dataset(file_name):
    dataset = []
    with open(file_name, "r") as data_file:
        for line in data_file:
            data_values = line.split(" ")
            label = float(data_values[1])
            temp = []
            for value in data_values[2:97]:
                    temp.append(float(value))
            instance = tuple(temp)
            dataset.append((instance, label))
        return dataset
