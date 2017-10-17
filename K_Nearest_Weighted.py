import random
import operator
from Helpers import euclidian_distance, load_dataset

class K_Nearest(object):
    """K nearest neighbor classifier"""

    def get_neighbors(self, k, trainingData, testDataItem):
        distances = []

        for i in range(len(trainingData)):
            distance = euclidean_distance(testDataItem, trainingData[i])

            if distance > 0: # avoid div by zero below
                distances.append((trainingSet[x], distance))

        distances.sort(key=operator.itemgetter(1))

        neighbors = []

        # collect k nearest neighbors
        for i in range(k):
            neighbors.append(distances[i][0])

        return neighbors

    def classify(self, instance):
        """Performs distance-weighted classification on the given instance"""
        classification = {}

        for i in range(len(instance)):
            category = instance[i][-1]
            if category in classification:
                classification[category] += (1 / category[1]) # contributes to class based on distance
            else:
                classification[category] = (1 / category[1]) # contributes to class based on distance

        sortedClassification = sorted(classification.iteritems(), 
                                    key=operator.itemgetter(1), 
                                    reverse=True)

        return sortedClassification[0][0]
