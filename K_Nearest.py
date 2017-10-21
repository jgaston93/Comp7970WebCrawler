import random
import operator
from Helpers import euclidian_distance
from Helpers import load_dataset

class K_Nearest(object):
    """K nearest neighbor classifier"""

    def __init__(self, k=3, distance_weighted=False, training_data=[], feature_mask =[1 for _ in range(95)]):
        self.k = k
        self.distance_weighted = distance_weighted
        self.training_data = training_data
        self.feature_mask = feature_mask
        self.neighbors = None
        random.seed(1716)

    def get_neighbors(self, instance):
        if self.neighbors is not None:
            # Only need to calculate neighbors once
            return self.neighbors

        distances = []

        for i in range(len(self.training_data)):
            distance = euclidian_distance(instance, self.training_data[i][0], self.feature_mask)
            distances.append((self.training_data[i], distance))

        distances.sort(key=operator.itemgetter(1))

        self.neighbors = []

        # collect k nearest neighbors
        for i in range(self.k):
            self.neighbors.append(distances[i][0])

    def load_data(self, training_data):
        """Loads new training data"""
        """training data format [(instance, label),(instance, label),...]"""
        self.training_data = training_data
		
    def set_feature_mask(self, feature_mask):
        """Used to apply a new feature mask to the classifier"""
        self.feature_mask = feature_mask

    def classify(self, instance):
        """Performs classification on the given instance"""
        
        self.get_neighbors(instance)

        classification = {1: 0, -1: 0}
        classificationWeighted = 0
        accumulatedCategory = 0
        accumulatedWeight = 0
		
        for neighbor in self.neighbors:
            category = neighbor[1]
            distance = neighbor[0][1]
            
            voteValue = 1 if not self.distance_weighted or distance == 0 else (1 / distance)

            classification[category] += voteValue
			
            if distance == 0:
                distance = 0.001
            accumulatedWeight += 1 / distance
            accumulatedCategory += (1 / distance)*category
        
        # return most frequently occuring neighbor
        if classification[1] == classification[-1]:
            if self.k == 1: # Fall back to random classification
                return 1 if random.randint(0, 1) == 1 else -1
            self.k -= 1
            return self.classify(instance)

        classificationWeighted = accumulatedCategory / accumulatedWeight
        if self.distance_weighted:
            return classificationWeighted

        return 1 if classification[1] > classification[-1] else -1
