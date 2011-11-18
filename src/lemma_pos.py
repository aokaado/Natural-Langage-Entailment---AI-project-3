from __future__ import division
import SentenceTree as st
import ResultPrinter as rp
import syn

class OneB:

	lemmaThresh = 0.7
	lemmaPosThresh = 0.625
	lemmaSynThresh = 0.73
	
	lemmaResult = {}
	lemmaPosResult = {}
	lemmaSynResult = {}
	
	def __init__(self, learnerfile = "../data/RTE2_dev.preprocessed.xml"):
		self.data = st.SentenceTree(learnerfile, False)
	
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
			for j in hlemmas.keys():
				if hpos.has_key(j):
					h = hlemmas[j]
					h2 = hpos[j]
					if h=="" or h2 =="":
						continue
					tot += 1
					#if h in tlemmas and h2 in tpos:
					#	count += 1
					for key in tlemmas.keys():
						if tlemmas[key] == h and tpos[key] == h2:
							count += 1
							break
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

	# Part IV		
	def matchLemmaSyn(self):
		lemma = {}
		for i in range(1, self.data.pairs+1):
			if i % 32 == 0:
				print i*100/800,"%"
			self.data.setCurrentId(i)
			count = 0
			tlemmas = self.data.getTextAttr("lemma")
			tSlemmas = [syn.Syn(t) for t in tlemmas]
			#print tSlemmas
			hlemmas = self.data.getHypAttr("lemma")
			tot = 0
			for h in hlemmas:
				if h in tlemmas:
					tot += 1
					count += 1
					#print "found xml lemma match"
				else:
					s = syn.Syn(h)
					if len(s.syns) > 0:
						tot += 1
						#print s.syns
						if syn.Syn(h) in tSlemmas:
							#print "found synonom match"
							count += 1
						#--------------Antonym
						if s.lemmas and tSlemmas
						s.lemmas[i].antonyms in 
						#--------------Antonym
					
			self.lemmaSynResult[i] = "YES" if count/tot > self.lemmaSynThresh else "NO"
			lemma[i] = count/tot
			#print lemma[i]
		return lemma
		
	def printResults(self, lemma = 0):
		if lemma == 0:
			if not self.lemmaResult:
				self.matchLemma()
			printer = rp.ResultPrinter()
			for key in self.lemmaResult.keys():
				printer.write(key, self.lemmaResult[key])
		elif lemma == 1:
			if not self.lemmaPosResult:
				self.matchLemmaPos()
			printer = rp.ResultPrinter()
			for key in self.lemmaPosResult.keys():
				printer.write(key, self.lemmaPosResult[key])
		elif lemma == 2:
			if not self.lemmaSynResult:
				self.matchLemmaSyn()
			printer = rp.ResultPrinter()
			for key in self.lemmaSynResult.keys():
				printer.write(key, self.lemmaSynResult[key])
		

if __name__ == "__main__":
	b = OneB()
	#print b.matchLemmaPos()
	b.printResults(2)
