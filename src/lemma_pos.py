from __future__ import division
import SentenceTree as st
import ResultPrinter as rp

class OneB:

	lemmaThresh = 0.70
	lemmaPosThresh = 0.70
	
	lemmaResult = {}
	lemmaPosResult = {}
	
	def __init__(self, learnerfile = "../data/RTE2_dev.preprocessed.xml"):
		self.data = st.SentenceTree(learnerfile, True)
	
	def matchLemmaPos(self):
		lemmap = {}
		for i in range(1, self.data.pairs+1):
			self.data.setCurrentId(i)
			count = 0
			tot = 0
			tlemmas = self.data.getTextAttrD("lemma")
			tpos = self.data.getTextAttrD("pos-tag")
			hlemmas = self.data.getHypAttrD("lemma")
			hpos = self.data.getHypAttrD("pos-tag")
			for j in range(1, self.data.textNodes()):
				if hlemmas.has_key(j) and hpos.has_key(j):
					h = hlemmas[j]
					h2 = hpos[j]
					if h=="" or h2 =="":
						continue
					tot += 1
					if h in tlemmas and h2 in tpos:
						count += 1
					
			self.lemmaPosResult[i] = "YES" if count/tot > self.lemmaPosThresh else "NO"
			lemmap[i] = count/tot
		return lemmap
	
	def matchLemma(self):
		lemma = {}
		for i in range(1, self.data.pairs+1):
			self.data.setCurrentId(i)
			count = 0
			tlemmas = self.data.getTextAttr("lemma")
			hlemmas = self.data.getHypAttr("lemma")
			for h in hlemmas:
				if h in tlemmas:
					count += 1
					
			self.lemmaResult[i] = "YES" if count/len(hlemmas) > self.lemmaThresh else "NO"
			lemma[i] = count/len(hlemmas)
		return lemma
		
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
