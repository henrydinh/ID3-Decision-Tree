#Henry Dinh - HxD130130
#CS 6375.001
#Assignment 1 - Decision Tree
#To test the program...

import sys
import csv

#Each set is a list of lists
#Index 0 of each list contains attribute name
#Last index is classification value
training_set = []
test_set = []
validation_set = []

#Calculates variance impurity (enropy)
#k = number of examples in training set
#k0 = number of training examples with class = 0
#k1 = number of training examples with class = 1
def calcVI(k, k0, k1):
    return (float(k0) / k) * (float(k1) / k)

#Calculates information gain
#x is an attribute
def calcIG(x):
    pass

def main(training_csv):
    #Use CSV reader to read csv files and store in lists
    with open(training_csv,'rb') as training_set:
        reader = csv.reader(training_set)
        training_set = list(reader)

    #k is number of examples in training set
    k = len(training_set) - 1
    #k0 is number of training examples with class = 0
    #k1 is number of training examples with class = 1
    k0 = 0
    k1 = 0
    for i in range(1, len(training_set)):
        if training_set[i][len(training_set[i]) - 1] == '0':
            k0 += 1
        elif training_set[i][len(training_set[i]) - 1] == '1':
            k1 += 1

    print "Stats for training set 1:"
    print "k = %d" % k
    print "k0 = %d" % k0
    print "k1 = %d" % k1
    print "VI(S) = %.4f" % calcVI(k, k0, k1) + "!"


if __name__ == '__main__':
    main(sys.argv[1])