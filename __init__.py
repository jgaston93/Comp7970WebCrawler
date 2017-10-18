from GRNN import GRNN
from K_Nearest import K_Nearest
from Validation import leave_one_out_validation
from Helpers import load_dataset
from Evolution_Module import Feature_Evolution


dataset = load_dataset("our_dataset.txt")
mask = []
#for c in "10100101010101011100110011111111100111100000111011011110000011001011110111100101101110101000111":
#    mask.append(int(c))
g = GRNN(standard_deviation = 0.24)
print(leave_one_out_validation(g, dataset))

kNN = K_Nearest()
print(leave_one_out_validation(kNN, dataset))

#Feature_Evolution(g, dataset)

#for i in range(168, 0, -1):
#        g.standard_deviation = i/10000
#        accuracy, tp, tn, fp, fn, mse = leave_one_out_validation(g, dataset)
#        print("std: {0} accuracy: {1}".format(i/10000, accuracy))
#        print("MSE: {0}".format(mse))
#        print("tp: {0} tn: {1} fp: {2} fn: {3}\n".format(tp, tn, fp, fn))
#        with open("std_test_results.csv", "a") as f:
#            f.write("{},{},{}\n".format(i/10000, accuracy, mse))