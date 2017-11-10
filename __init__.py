from GRNN import GRNN
import Validation
from Helpers import load_dataset
from Evolution_Module import Feature_Evolution, Feature_Vector_Evolution
import random


#dataset = load_dataset("trainingset_st.csv")
dataset = load_dataset("our_dataset.txt")
#feature_count = 0
#feature_mask = []
#features = []
#10001011111110100101100100011101
#011010001001110011100010010001011101000010011101101110110000011101110001010110010110100111111110011100101010100111010110110100011010101010001101

#100100110101010100000101111111110101010110011110111100110001100001110011010011100110001111110100110001101100011010101111010111100010010011001010
#with open("FeatureNames.txt", "r") as f:
#    for feature,c in zip(f,"100100110101010100000101111111110101010110011110111100110001100001110011010011100110001111110100110001101100011010101111010111100010010011001010"):
#        feature_mask.append(int(c))
#        if c == "1":
#            features.append(feature)
#            feature_count += 1

#print(feature_count)
g = GRNN(training_data=dataset)
#print(Validation.leave_one_out_validation_aa(g, dataset))
filename = "GA_Results"
for i in range(10):
    Feature_Vector_Evolution(g,filename + str(i), 2**i)
#Feature_Evolution(g, dataset, population = 100, num_children = 20, num_features = 176, generations = 8000)
#with open("std_test_results.csv", "w") as f:
#            f.write("{},{},{}\n".format(i/100, accuracy, mse))
#for i in range(700, -1, -1):
#        g.standard_deviation = i/10000
#        accuracy= Validation.leave_one_out_validation_aa(g, dataset)
#        print("std: {0} accuracy: {1}\n".format(i/10000, accuracy))
        #with open("std_sa_results.csv", "a") as f:
        #    f.write("{},{}\n".format(i/100, accuracy))
