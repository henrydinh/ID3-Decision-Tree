# Henry Dinh - HxD130130
# CS 6375.001
# Assignment 1 - Decision Tree
# To test the program...

import sys
import csv

# Each set is a list of lists
# Index 0 of each list contains attribute name
# Last index is classification value
training_set = []
test_set = []
validation_set = []


# Calculates variance impurity (enropy), VI(S)
# k = number of examples in training set
# k0 = number of training examples with class = 0
# k1 = number of training examples with class = 1
def calcVI(k, k0, k1):
    print "k: %d" % k
    return (float(k0) / k) * (float(k1) / k)


# Calculates information gain, Gain(S:X)
# S is the data set and x is an attribute
# entropy is the VI of the parent node
def calcIG(entropy, data_set, attr_col_num):
    gain = 0.00
    count_1_1 = 0  # Counts attributes with 1 value and class 1
    count_1_0 = 0  # Counts attributes with 1 value and class 0
    count_0_1 = 0  # Counts attributes with 0 value and class 1
    count_0_0 = 0  # Counts attributes with 0 value and class 0
    for i in range(1, len(data_set)):
        if data_set[i][attr_col_num] == '0':
            if data_set[i][len(data_set[i]) - 1] == '0':
                count_0_0 += 1
            else:
                count_0_1 += 1
        else:
            if data_set[i][len(data_set[i]) - 1] == '0':
                count_1_0 += 1
            else:
                count_1_1 += 1
    print count_0_0
    print count_0_1
    print count_1_0
    print count_1_1
    num_examples = count_0_0 + count_0_1 + count_1_0 + count_1_1
    # Calculates VI(Sx) for attribute value 1
    oneVI = calcVI(count_1_1 + count_1_0, count_1_0, count_1_1)
    print "oneVI: %.4f" % oneVI
    # Calculates VI(Sx) for attribute value 0
    zeroVI = calcVI(count_0_1 + count_0_0, count_0_0, count_0_1)
    print "zeroVI: %.4f" % zeroVI
    gain = entropy - (((count_1_1 + count_1_0) / float(num_examples)) * oneVI) - \
           (((count_0_1 + count_0_0) / float(num_examples)) * zeroVI)
    return gain


def main(training_csv):
    # Use CSV reader to read csv files and store in lists
    with open(training_csv, 'rb') as training_set:
        reader = csv.reader(training_set)
        training_set = list(reader)

    # k is number of examples in training set
    k = len(training_set) - 1
    # k0 is number of training examples with class = 0
    # k1 is number of training examples with class = 1
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
    entropy = calcVI(k, k0, k1)
    print "VI(S) = %.4f" % entropy + "\n"

    for i in range(0, len(training_set[0]) - 1):
        print "Gain for attr %s, %d: %.6f" % (training_set[0][i],i, calcIG(entropy, training_set, i)) + "\n"



if __name__ == '__main__':
    main(sys.argv[1])
