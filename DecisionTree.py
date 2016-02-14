# Henry Dinh - HxD130130
# CS 6375.001
# Assignment 1 - ID3 Decision Tree Implementation
# To test the program, read the README file.

import csv
import sys
from random import randint

# Each set is a list of lists
# Index 0 of each list contains attribute name
# Last index is classification value
training_set = []
training_set_attributes = []
training_set_instances = []

validation_set = []
validation_set_attributes = []
validation_set_instances = []

test_set = []
test_set_attributes = []
test_set_instances = []


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
        # Find gain for each attribute except last one, which is the classification
        for i in range(0, len(attributes) - 1):
            gain = calcIG(entropy, data_set, i)
            if gain > highest_gain:
                highest_gain = gain
                attr_index_most_gain = i
        root.set_label(attributes[attr_index_most_gain])
        attributes.pop(attr_index_most_gain)
        # Left is subset of instances with chosen attribute having value 0
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


# Counts number of non-leaf nodes
def countNonLeafNodes(root_node):
    if root_node is None or (root_node.get_left0() is None and root_node.get_right1() is None):
        return 0
    return 1 + countNonLeafNodes(root_node.get_left0()) + countNonLeafNodes(root_node.get_right1())


# Orders (number) non-leaf nodes from 1 to number of non-leaf nodes
# n is list of numbers to give to nodes. already_numbered keeps tracks of nodes already numbered..
def orderNonLeafNodes(root_node, n, already_numbered):
    if root_node.get_left0() is not None and root_node.get_left0() != '1' and root_node.get_left0() != '0':
        orderNonLeafNodes(root_node.get_left0(), n, already_numbered)
        if n and root_node.get_label() not in already_numbered:
            root_node.set_number(n.pop())
            already_numbered.append(root_node.get_label())
    if root_node.get_right1() is not None and root_node.get_right1() != '1' and root_node.get_right1() != '0':
        orderNonLeafNodes(root_node.get_right1(), n, already_numbered)
        if n and root_node.get_label() not in already_numbered:
            root_node.set_number(n.pop())
            already_numbered.append(root_node.get_label())


# Post pruning algorithm
def postPrune(d, l, k):
    d_best = d
    for i in range(1, l + 1):
        d_prime = d
        m = randint(1, k)
        for j in range(1, m + 1):
            # n is number of non-leaf nodes in the decision tree d_prime
            n = countNonLeafNodes(d_prime)
            # Order non-leaf nodes in D' from 1 to n
            nonleaf_nodes_nums = []
            for z in range(1, n + 1):
                nonleaf_nodes_nums.append(z)
            orderNonLeafNodes(d_prime, nonleaf_nodes_nums, list())
            p = randint(1, n)


# Nodes class for decision tree nodes. Root node has "None" for parent
# Left branch is for attribute value 0 and right is for 1
class Node:
    # Initially node has None for parent node, and left and right branches
    left0 = None
    right1 = None
    # Attribute name of the node
    label = None
    # Number for post pruning later
    number = None

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

    def set_number(self, value):
        self.number = value

    def get_number(self):
        return self.number


def main(training_csv):
    # Use CSV reader to read csv files and store in lists
    with open(training_csv, 'rb') as training_set:
        reader = csv.reader(training_set)
        training_set = list(reader)

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

    print "Stats for the training set, S:"
    print "Total instances = %d" % k
    print "Instances with class 0 = %d" % k0
    print "Instances with class 1 = %d" % k1
    entropy = calcVI(k, k0, k1)
    print "VI(S) = %.4f" % entropy + "\n"

    # Build the decision tree and print it with correct format
    id3_tree = buildID3(training_set_instances, training_set_attributes)
    print "Decision tree before pruning: ",
    printTree(id3_tree, 0)


if __name__ == '__main__':
    main(sys.argv[1])
