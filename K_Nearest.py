import random
import operator
from Helpers import euclidian_distance, load_dataset

class K_Nearest(object):
    """K nearest neighbor classifier"""

    def __init__(self, distance_weighted=False, training_data=[], feature_mask =[1 for _ in range(95)]):
        self.distance_weighted = distance_weighted
        self.training_data = training_data
        self.feature_mask = feature_mask

    def get_neighbors(self, k, trainingData, testDataItem):
        distances = []

        for i in range(len(trainingData)):
            distance = euclidean_distance(testDataItem, trainingData[i])
            distances.append((trainingSet[x], distance))

        distances.sort(key=operator.itemgetter(1))

        neighbors = []

        # collect k nearest neighbors
        for i in range(k):
            neighbors.append(distances[i][0])

        return neighbors

    def load_data(self, training_data):
        """Loads new training data"""
        """training data format [(instance, label),(instance, label),...]"""
        self.training_data = training_data

    def classify(self, instance):
        """Performs classification on the given instance"""
        classification = {}

        for training_instance in self.training_data:
            category = training_instance[1]
            voteValue = (1 / category[1]) if self.distance_weighted else 1
            if category in classification:
                classification[category] += voteValue
            else:
                classification[category] = voteValue

        sortedClassification = sorted(classification.iteritems(), 
                                    key=operator.itemgetter(1), 
                                    reverse=True)

        instanceClass = 1 if classification[1] > classification[-1] else -1

        # return most frequently occuring neighbor
        return instanceClass
