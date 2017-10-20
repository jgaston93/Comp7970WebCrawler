from GRNN import GRNN
from Validation import leave_one_out_validation
from Helpers import load_dataset
from Evolution_Module import Feature_Evolution


dataset = load_dataset("our_dataset.txt")
feature_count = 0
for c in "00110101101111110000111011101110010011001111001010011001101011111110110111110101101011110011111":
    if c == "1":
        feature_count = feature_count + 1

print(feature_count)
#g = GRNN(training_data=dataset, standard_deviation = 0.0201)
#print(leave_one_out_validation(g, dataset))
#print(g.numZeros)
#Feature_Evolution(g, dataset, population = 20, num_children = 6)

#for i in range(30, -1, -2):
#        g.standard_deviation = i/1000
#        accuracy, tp, tn, fp, fn, mse = leave_one_out_validation(g, dataset)
#        print("std: {0} accuracy: {1}".format(i/1000, accuracy))
#        print("MSE: {0}".format(mse))
#        print("tp: {0} tn: {1} fp: {2} fn: {3}\n".format(tp, tn, fp, fn))
#        with open("std_test_results.csv", "a") as f:
#            f.write("{},{},{}\n".format(i/1000, accuracy, mse))