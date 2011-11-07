from __future__ import division
import SentenceTree as st
import ResultPrinter as rp

class OneB:

	lemmaThresh = 0.4
	lemmaPosThresh = 0.4
	
	lemmaResult = {}
	lemmaPosResult = {}
	
	def __init__(self):
		self.data = st.SentenceTree()
	
	def matchPairs(self):
		for i in range(1, self.data.pairs+1):
			self.data.setCurrentId(i)
			count = 0
			tlemmas = self.data.getTextAttr("lemma")
			hlemmas = self.data.getHypAttr("lemma")
			for t in tlemmas:
				if t in hlemmas:
					count += 1
					
			self.lemmaResult[i] = "YES" if count/len(tlemmas) > self.lemmaThresh else "NO"
		
	def printResults(self):
		if not self.lemmaResult:
			self.matchPairs()
		printer = rp.ResultPrinter()
		for key in self.lemmaResult.keys():
			printer.write(key, self.lemmaResult[key])
			
