"""Module for GRNN classifier"""
import math
import random
from Helpers import euclidian_distance

class GRNN(object):
    """GRNN classifier"""

    def __init__(self, training_data=[], standard_deviation=0.11853, feature_mask =None):
        self.training_data = training_data
        if feature_mask == None:
            self.feature_mask = [1 for _ in range(len(training_data[0][0]))]
        else:
            self.feature_mask = feature_mask
        self.standard_deviation = standard_deviation

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