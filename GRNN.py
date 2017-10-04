"""Module for GRNN classifier"""

def euclidian_distance(vector1, vector2):
	"""Calculates the euclidian distance between two vectors"""
    result = 0
    for x_value, y_value in zip(vector1, vector2):
        result = result + (y_value - x_value)**2
    return result**(1/2)

class GRNN(object):
    """GRNN classifier"""

    def __init__(self, neurons=[], weights=[], standard_deviation=1.41):
        self.neurons = neurons
        self.weights = weights
        self.standard_deviation = standard_deviation

    def _h_function(self, t_q, t_i):
        distance = _euclidian_distance(t_i, t_q)
        return math.e**(-distance/(2*self.standard_deviation**2))

    def classify(self, instance):
        """Performs classification on the given instance"""
        numerator = 0
        denominator = 0
        for neuron, weight in zip(self.neurons, self.weights):
            h_value = self._h_function(instance, neuron)
            numerator = numerator + h_value*weight
            denominator = denominator + h_value
        return numerator/denominator
