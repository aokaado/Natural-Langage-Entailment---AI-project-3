import orange, orngTest, orngStat, orngTree

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
results = orngTest.crossValidation(learners, data, folds=10)
print results
# output the results
print "Learner  CA     IS     Brier    AUC"
for i in range(len(learners)):
    print "%-8s %5.3f  %5.3f  %5.3f  %5.3f" % (learners[i].name, \
        orngStat.CA(results)[i], orngStat.IS(results)[i],
        orngStat.BrierScore(results)[i], orngStat.AUC(results)[i])
