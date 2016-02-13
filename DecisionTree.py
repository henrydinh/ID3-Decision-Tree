# Henry Dinh - HxD130130
# CS 6375.001
# Assignment 1 - Decision Tree
# To test the program...

import csv
import sys

# Each set is a list of lists
# Index 0 of each list contains attribute name
# Last index is classification value
training_set = []
training_set_attributes = []
training_set_instances = []
test_set = []
validation_set = []


# Calculates variance impurity (enropy), VI(S)
# k = number of examples in training set
# k0 = number of training examples with class = 0
# k1 = number of training examples with class = 1
def calcVI(k, k0, k1):
    return (float(k0) / k) * (float(k1) / k)


# Calculates information gain, Gain(S:X)
# S is the data set and x is an attribute
# entropy is the VI of the parent node
# note data_set means the set where examples have parent node's attribute vale
# i.e. examples that have parent node's attribute value = 1
def calcIG(entropy, data_set, attr_col_num):
    gain = 0.00
    count_1_1 = 0  # Counts attributes with 1 value and class 1
    count_1_0 = 0  # Counts attributes with 1 value and class 0
    count_0_1 = 0  # Counts attributes with 0 value and class 1
    count_0_0 = 0  # Counts attributes with 0 value and class 0
    for i in range(0, len(data_set)):
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
    num_examples = count_0_0 + count_0_1 + count_1_0 + count_1_1
    # Calculates VI(Sx) for attribute value 1
    oneVI = 0.00
    if (count_1_1 + count_1_0) == 0:
        oneVI = 0.00
    else:
        oneVI = calcVI(count_1_1 + count_1_0, count_1_0, count_1_1)
    # Calculates VI(Sx) for attribute value 0
    zeroVI = 0.00
    if (count_0_1 + count_0_0) == 0:
        zeroVI = 0.00
    else:
        zeroVI = calcVI(count_0_1 + count_0_0, count_0_0, count_0_1)
    gain = entropy - (((count_1_1 + count_1_0) / float(num_examples)) * oneVI) - \
           (((count_0_1 + count_0_0) / float(num_examples)) * zeroVI)
    return gain


# Checks if all instances in data set have same same value for classification
# true means all instances with that attribute value have the same classification
def checkAttrClassification(data_set):
    num_1 = 0
    num_0 = 0
    for i in range(0, len(data_set)):
        if data_set[i][len(data_set[i]) - 1] == '1':
            num_1 += 1
        else:
            num_0 += 1
    if num_1 == 0 or num_0 == 0:
        return True
    else:
        return False


# Returns most common classification for set of instances
def mostCommonClass(data_set):
    num_1 = 0
    num_0 = 0
    for i in range(0, len(data_set)):
        if data_set[i][len(data_set[i]) - 1] == '1':
            num_1 += 1
        else:
            num_0 += 1
    if num_1 >= num_0:
        return '1'
    else:
        return '0'


# Counts number of instances with class = 1
def class1(data_set):
    count = 0
    for i in range(0, len(data_set)):
        if data_set[i][len(data_set[i]) - 1] == '1':
            count += 1
    return count


# Counts number of instances with class =0
def class0(data_set):
    count = 0
    for i in range(0, len(data_set)):
        if data_set[i][len(data_set[i]) - 1] == '0':
            count += 1
    return count


# Builds ID3 decision tree recursively. Returns the root node of the tree
# data_set is set of instances and attributes is the list of attributes being tested/remaining (reduced througout)
def buildID3(data_set, attributes):
    root = Node(None)
    print attributes
    if checkAttrClassification(data_set):
        # if all instances have same value for classification, \
        # return this single node (leaf) with classification value (0 or 1)
        root.set_label(data_set[0][len(data_set[0]) - 1])
    elif len(attributes) == 1:
        # No more attributes to test. Only attribute left in attributes left is the classification
        root.set_label(mostCommonClass(data_set))
    else:
        # find attribute column number (index) wih most gain
        highest_gain = 0.00
        attr_index_most_gain = 0
        # find entropy for current node attribute
        entropy = calcVI(len(data_set), class0(data_set), class1(data_set))
        print "Current entropy: %.4f" % entropy
        # Find gain for each attribute except last one, which is the classification
        for i in range(0, len(attributes) - 1):
            gain = calcIG(entropy, data_set, i)
            if gain > highest_gain:
                highest_gain = gain
                attr_index_most_gain = i
        root.set_label(attributes[attr_index_most_gain])
        attributes.pop(attr_index_most_gain)
        # Left is subset of instances with chosen attribute having value 0
        print "doing left"
        left = []
        for i in range(0, len(data_set)):
            if data_set[i][attr_index_most_gain] == '0':
                left.append(data_set[i])
        if not left:
            # Make leaf node
            root.set_left0(Node(mostCommonClass(left)))
        else:
            # Make new subtree
            root.set_left0(buildID3(left, attributes))
        # Right is subset of instances with chosen attribute having value 1
        print "Doing right"
        right = []
        for i in range(0, len(data_set)):
            if data_set[i][attr_index_most_gain] == '1':
                right.append(data_set[i])
        if not right:
            # Make leaf node
            root.set_right1(Node(mostCommonClass(right)))
        else:
            # Make new subtree
            root.set_right1(buildID3(right, attributes))
    return root


def printTree(root_node, level):
    if root_node.get_label() == '0' or root_node.get_label() == '1':
        # Print leaf node
        print root_node.get_label(),
    else:
        # Print attribute (internal) nodes
        # Print left side (0) first and then right side (1)
        print
        for i in range(0, level):
            print "|",
        print "%s = 0 : " % (root_node.get_label()),
        printTree(root_node.get_left0(), level + 1)
        print
        for i in range(0, level):
            print "|",
        print "%s = 1 : " % (root_node.get_label()),
        printTree(root_node.get_right1(), level + 1)


# Nodes class for decision tree nodes. Root node has "None" for parent
# Left branch is for attribute value 0 and right is for 1
class Node:
    # Initially node has None for parent node, and left and right branches
    left0 = None
    right1 = None
    # Attribute name of the node
    label = None

    def __init__(self, label):
        self.label = label

    def set_label(self, value):
        self.label = value

    def get_label(self):
        return self.label

    # left branch can be another attribute or a leaf where classification = 0 or 1
    def set_left0(self, value):
        self.left0 = value

    def get_left0(self):
        return self.left0

    # right branch can be another attribute or a leaf where classification = 0 or 1
    def set_right1(self, value):
        self.right1 = value

    def get_right1(self):
        return self.right1


def main(training_csv):
    # Use CSV reader to read csv files and store in lists
    with open(training_csv, 'rb') as training_set:
        reader = csv.reader(training_set)
        training_set = list(reader)

    # Make list for attribute names and list for instances
    training_set_attributes = training_set[0]
    for i in range(1, len(training_set)):
        training_set_instances.append(training_set[i])

    # k is number of examples in training set
    k = len(training_set_instances)
    # k0 is number of training examples with class = 0
    # k1 is number of training examples with class = 1
    k0 = 0
    k1 = 0
    for i in range(0, len(training_set_instances)):
        if training_set_instances[i][len(training_set_instances[i]) - 1] == '0':
            k0 += 1
        elif training_set_instances[i][len(training_set_instances[i]) - 1] == '1':
            k1 += 1

    print "Stats for training set 1:"
    print "k = %d" % k
    print "k0 = %d" % k0
    print "k1 = %d" % k1
    entropy = calcVI(k, k0, k1)
    print "VI(S) = %.4f" % entropy + "\n"

    for i in range(0, len(training_set_attributes)):
        print "Gain for attr %s, %d: %.6f" % (
            training_set_attributes[i], i, calcIG(entropy, training_set_instances, i)) + "\n"

    id3_tree = buildID3(training_set_instances, training_set_attributes)
    printTree(id3_tree, 0)


if __name__ == '__main__':
    main(sys.argv[1])
