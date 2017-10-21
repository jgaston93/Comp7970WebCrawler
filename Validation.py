"""This module contains the validation functions to test accuracy"""

def leave_one_out_validation(classifier, data_set):
    """This function is the leave one out validation"""
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    squared_errors = []
    for index in range(len(data_set)):
        training_set = data_set[0:index] + data_set[index+1:]
        validation_instance = data_set[index]
        classifier.load_data(training_set)
        classification_result = classifier.classify(validation_instance[0])
        squared_errors.append((classification_result - validation_instance[1])**2)
        if classification_result >= 0:
            if validation_instance[1] > 0:
                true_positive = true_positive + 1
            else:
                false_positive = false_positive + 1
        elif classification_result < 0:
            if validation_instance[1] > 0:
                false_negative = false_negative + 1
            else:
                true_negative = true_negative + 1
    accuracy = (true_positive + true_negative)/(true_positive + true_negative + false_positive + false_negative)
    mean_squared_error = 0
    for squared_error in squared_errors:
        mean_squared_error = mean_squared_error + squared_error
    mean_squared_error = mean_squared_error/len(squared_errors)
    return accuracy, true_positive, true_negative, false_positive, false_negative, mean_squared_error
        
