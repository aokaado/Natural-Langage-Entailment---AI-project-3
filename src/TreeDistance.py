from __future__ import division
import treeEdit as td
import SentenceTree as st
import ResultPrinter as rp

def weighter(node1, node2):
	"""
	Defines unit cost for edit operation on pair of nodes,
	i.e. cost of insertion, deletion, substitution are all 1
	"""
	# insertion cost
	if node1 is None:
		if node2.label in ["ABSTRACT", "ROOT"]:
			return 0
		#print "label ", node2.label, tdi.data.getDf(node2.label, "lemma")
		return tdi.data.getDf(node2.label, "lemma")

	# deletion cost
	if node2 is None:
		return 0

	# substitution cost
	if node1.label != node2.label:
		#if node1.label in ["ABSTRACT", "ROOT"] and node2.label in ["ABSTRACT", "ROOT"]:
		#	return 0
		#return (tdi.data.getDf(node1.label, "lemma")+tdi.data.getDf(node2.label, "lemma"))/2
		return 1
	return 0

class TreeDistance:
	
	#thresh = 0.625
	thresh = 0.425
	
	def __init__(self):
		self.data = st.SentenceTree(True)
		self.result = {}
		
	def getTrees(self):
		self.data.setCurrentId(23)
		#for item in self.data.getTextTrees():
		#for itemtwo in self.data.getHypTrees():
		
		item = self.data.getTextTree()
		itemtwo = self.data.getHypTree()
		print "ONE ", item, "\nTWO ",  itemtwo
		dist = td.distance(item, itemtwo, weighter)
		empty = td.Node("TEST")
		norm = td.distance(empty, itemtwo, weighter)
		print "distance ", dist, "normalisation ", norm, " fin ", (norm-dist)/norm

	def matchTrees(self, weight = False ):
		for i in range(1, self.data.pairs+1):
			if i % 8 == 0:
				print i*100/800,"%"
			self.data.setCurrentId(i)
			tTree = self.data.getTextTree()
			hTree = self.data.getHypTree()
			empty = td.Node("EMPTY")

			if weight:
				dist = td.distance(tTree, hTree, weighter)
				norm = td.distance(empty, hTree, weighter)
			else:
				dist = td.distance(tTree, hTree)
				norm = td.distance(empty, hTree)
			
			self.result[i] = "YES" if (norm-dist)/norm > self.thresh else "NO"
			
	
	def printResults(self):
		if not self.result:
			self.matchTrees()
		printer = rp.ResultPrinter()
		for key in self.result.keys():
			printer.write(key, self.result[key])
			
td.deletion_cost = 0
tdi = TreeDistance()
#tdi.getTrees()
tdi.matchTrees(True)
tdi.printResults()
