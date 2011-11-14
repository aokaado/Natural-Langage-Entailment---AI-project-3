from __future__ import division
import treeEdit as td
import SentenceTree as st

class TreeDistance:
	
	def __init__(self):
		self.data = st.SentenceTree()
	
	def getTrees(self):
		self.data.setCurrentId(65)
		#for item in self.data.getTextTrees():
		#for itemtwo in self.data.getHypTrees():
		
		item = self.data.getTextTrees()
		itemtwo = self.data.getHypTrees()
		print "ONE ", item, "\nTWO ",  itemtwo
		dist = td.distance(item, itemtwo)
		empty = td.Node("TEST")
		norm = td.distance(empty, itemtwo)
		print "distance ", dist, "normalisation ", norm, " fin ", dist/norm
		
		
td.deletion_cost = 0
tdi = TreeDistance()
tdi.getTrees()
