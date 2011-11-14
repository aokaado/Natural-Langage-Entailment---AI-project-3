from __future__ import division
import SentenceTree as st
import ResultPrinter as rp

class OneB:

	lemmaThresh = 0.70
	lemmaPosThresh = 0.69
	
	lemmaResult = {}
	lemmaPosResult = {}
	
	def __init__(self):
		self.data = st.SentenceTree()
	
	def matchLemmaPos(self):
		for i in range(1, self.data.pairs+1):
			self.data.setCurrentId(i)
			count = 0
			tlemmas = self.data.getTextAttr("lemma")
			tpos = self.data.getTextAttr("pos-tag")
			hlemmas = self.data.getHypAttr("lemma")
			hpos = self.data.getHypAttr("pos-tag")
			for j in range(1, self.data.textNodes()):
				t = tlemmas[j]
				t2 = tpos[j]
				if t in hlemmas and t2 in hpos:
					count += 1
					
			self.lemmaPosResult[i] = "YES" if count/len(hlemmas) > self.lemmaPosThresh else "NO"
	
	def matchLemma(self):
		for i in range(1, self.data.pairs+1):
			self.data.setCurrentId(i)
			count = 0
			tlemmas = self.data.getTextAttr("lemma")
			hlemmas = self.data.getHypAttr("lemma")
			for t in tlemmas:
				if t in hlemmas:
					count += 1
					
			self.lemmaResult[i] = "YES" if count/len(hlemmas) > self.lemmaThresh else "NO"
		
	def printResults(self, lemma = True):
		if lemma:
			if not self.lemmaResult:
				self.matchLemma()
			printer = rp.ResultPrinter()
			for key in self.lemmaResult.keys():
				printer.write(key, self.lemmaResult[key])
		else:
			if not self.lemmaPosResult:
				self.matchLemmaPos()
			printer = rp.ResultPrinter()
			for key in self.lemmaPosResult.keys():
				printer.write(key, self.lemmaPosResult[key])
