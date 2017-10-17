import random
import operator
from Helpers import euclidian_distance, load_dataset

class K_Nearest(object):
    """K nearest neighbor classifier"""

    def __init__(self, training_data=[], feature_mask =[1 for _ in range(95)]):
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

        for i in range(len(instance)):
            category = instance[i][-1]
            if category in classification:
                classification[response] += 1
            else:
                classification[response] = 1

        sortedClassification = sorted(classification.iteritems(), 
                                    key=operator.itemgetter(1), 
                                    reverse=True)

        # return most frequently occuring neighbor
        return sortedClassification[0][0]
