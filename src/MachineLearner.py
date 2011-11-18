from __future__ import division
import random
import orange, orngTest, orngStat, orngTree
import os
import FeaturePrinter as fp

# If there is no feature file, create it
if not os.path.exists("features.tab"):
	fp.createFile()
	
	
class CrossVal:
	acc = []
	
	def __init__(self, data, folds = 40, k = 150):
		self.data = data
		self.folds = folds
		self.k = k
		
	def knn(self):
		random.seed()
		seed = int(random.random()*1000)
		rndind = orange.MakeRandomIndices2(self.data, p0=(self.folds-1)/self.folds, randseed = seed)

		train = data.select(rndind, 0)
		test = data.select(rndind, 1)
		knn = orange.kNNLearner(train, self.k)
		
		occ = 0
		for inp in test:
			if knn(inp) == inp.getclass():
				occ += 1
		ca = occ/len(test)
		self.acc.append(ca)
		
	def run_kNN(self):
		for i in range(0, self.folds):
			cv.knn()
			
	def CA(self):
		return sum(self.acc)/len(self.acc)
		
	def printCA(self):
		print "Accuracy of kNN classifier is %5.3f%%" % (self.CA()*100)
		
		
data = orange.ExampleTable("features.tab")
folds = 10
k = 150
cv = CrossVal(data, folds, k)
cv.run_kNN()
cv.printCA()


# Builtin ClossValidator, with several classifiers
if False:
	# set up the learners
	bayes = orange.BayesLearner()
	tree = orngTree.TreeLearner(mForPruning=2)
	knn = orange.kNNLearner(k=150)
	bayes.name = "bayes"
	tree.name = "tree"
	knn.name = "knn"
	learners = [bayes, tree, knn]

	# compute accuracies on data
	data = orange.ExampleTable("features.tab")

	# Create a crossvalidation on the sampleset so that you don't classify it's own data
	results = orngTest.crossValidation(learners, data, folds=10)

	# output the results
	print "Learner \tAccuracy"
	for i in range(len(learners)):
		print "%-8s\t%5.3f%%" % (learners[i].name, orngStat.CA(results)[i]*100)
