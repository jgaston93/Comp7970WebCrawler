"""Module for GRNN classifier"""
import math
import random
from Helpers import euclidian_distance

class GRNN(object):
    """GRNN classifier"""

    def __init__(self, training_data=[], standard_deviation=1.41, feature_mask =None, global_method=True, k=1):
        self.training_data = training_data
        if feature_mask == None:
            self.feature_mask = [1 for _ in range(len(training_data[0][0]))]
        else:
            self.feature_mask = feature_mask
        self.standard_deviation = standard_deviation
        if not global_method:
            self.clusters = self._k_means_cluster_creator(training_data, k)

    def _argmin(self, elements):
        index = 0
        value = elements[0]
        current_index = 0
        for element in elements:
            if element < value:
                index = current_index
                value = element
            current_index = current_index + 1
        return index

    def _k_means_cluster_creator(self, data_points, k):
        clusters = []
        centroids = random.sample(data_points, k)
        for i in range(5):
            clusters = [[] for _ in range(k)]
            for point in data_points:
                distances = []
                for centroid in centroids:
                    distances.append(euclidian_distance(centroid[0], point[0]))
                min_index = self._argmin(distances)
                clusters[min_index].append(point)
            for centroid_index in range(k):
                new_center = [0 for _ in range(95)]
                for point in clusters[centroid_index]:
                    for j in range(95):
                        new_center[j] = new_center[j] + point[0][j]
                    for j in range(95):
                        new_center[j] = new_center[j]/len(clusters[centroid_index])
                centroids[centroid_index] = (tuple(new_center), 0)
        return clusters

    def _h_function(self, t_q, t_i):
        # calculate the h value using the masked features
        distance = euclidian_distance(t_i, t_q, self.feature_mask)
        return math.e**(-(distance**2)/(2*self.standard_deviation**2))

    def set_feature_mask(self, feature_mask):
        """Used to apply a new feature mask to the classifier"""
        self.feature_mask = feature_mask

    def load_data(self, training_data):
        """Loads new training data"""
        """training data format [(instance, label),(instance, label),...]"""
        self.training_data = training_data

    def classify(self, instance):
        """Performs classification on the given instance"""
        numerator = 0
        denominator = 0
        for training_instance in self.training_data:
            h_value = self._h_function(instance, training_instance[0])
            numerator = numerator + h_value*training_instance[1]
            denominator = denominator + h_value
        return numerator/denominator