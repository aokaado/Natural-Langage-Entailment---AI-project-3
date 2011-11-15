from __future__ import division
from xml.etree.cElementTree import iterparse
import Pair as p
import ResultPrinter as rp
import eval_rte
import SentenceTree as st

class WordMatcher:
	threshHold = 0.4
	weightedThreshHold = 0.325
	result = -1
	pairs = {}
	weight = False

	def __init__(self, inf, weighting = False):#t, h, idx):
		currentPair = p.Pair()
		currentID = 0
		for event, elem in iterparse(inf):
			if elem.tag == "t":
				currentPair.text = elem.text.lower().split(" ")
			if elem.tag == "h":
				currentPair.hypothesis = elem.text.lower().split(" ")
			if elem.tag == "pair":
				#print elem.get("id")
				#print "in init: ", currentPair.text, ", ", currentPair.result, ", ", currentPair.hypothesis 
				self.pairs[int(elem.get("id"))] = currentPair
				currentPair = p.Pair()
		if weighting:
			self.weight = True
			self.thresh = self.weightedThreshHold
			self.weighter = st.SentenceTree()
		else:
			self.thresh = self.threshHold
		
	def match(self, i): # i is id of pair
		return self.simpleMatch(i)
		
	def simpleMatch(self, i): # i is id of pair
		occ = 0.0
		currentPair = self.pairs[i]
		hyplen = 0.0
		for word in currentPair.hypothesis:
			if self.weight:
				hyplen += self.weighter.getDf(word)
			else:
				hyplen +=1.0
			if word in currentPair.text:
					if self.weight:
						occ +=self.weighter.getDf(word)
					else:
						occ +=1.0
		#print "occ: ", occ, "len: ", hyplen
		currentPair.result = occ/hyplen
	
	def isGood(self, i): # i is id of pair
		currentPair = self.pairs[i]
		if currentPair.result < 0:
			self.match(i)
		return "YES" if currentPair.result >= self.thresh else "NO"
		
	def verbose(self, i): #i is id of pair
		#print "in verbose: ", self.pairs[i].text, ", ", self.pairs[i].result, ", ", self.pairs[i].hypothesis 
		if self.pairs[i].result < 0:
			self.match(i)
		#print "%.2f" % (self.pairs[i].result*100), "% is a", self.isGood(i)

	def getFeatures(self):
		res = {}
		for i in range(1, len(self.pairs)+1):
			res[i] = self.pairs[i].result
		return res

if __name__ == "__main__":
	#test
	# if weighting applied, add True, else False or nothing
	wordtest = WordMatcher("../data/RTE2_dev.xml", True)
	resultP = rp.ResultPrinter()
	for i in range(1, len(wordtest.pairs)+1):
		if i % 32 == 0:
			print i*100/800,"%"
		wordtest.verbose(i)
		resultP.write(i, wordtest.isGood(i))
