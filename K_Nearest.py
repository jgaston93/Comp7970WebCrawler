import random
import operator
from Helpers import euclidian_distance, load_dataset

class K_Nearest(object):
    """K nearest neighbor classifier"""

    def get_neighbors(self, k, trainingData, testDataItem):
        distances = []

        for i in range(len(trainingData)):
            distance = euclidean_distance(testDataItem, trainingData[i])
            distances.append((trainingSet[x], dist))

        distances.sort(key=operator.itemgetter(1))

        neighbors = []

        for i in range(k):
            neighbors.append(distances[i][0])

        return neighbors

    def classify(self, instance):
        """Performs classification on the given instance"""
        classification = {}

        for i in range(len(instance)):
            category = instance[x][-1]
            if category in classification:
                classification[response] += 1
            else:
                classification[response] = 1

        sortedClassification = sorted(classification.iteritems(), 
                                    key=operator.itemgetter(1), 
                                    reverse=True)
        return sortedVotes[0][0]

load_dataset('our_dataset.txt')
