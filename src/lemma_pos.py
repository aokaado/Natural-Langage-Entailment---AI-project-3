from __future__ import division
import SentenceTree as st
import ResultPrinter as rp
import syn

class OneB:

	lemmaThresh = 0.7
	lemmaPosThresh = 0.625
	lemmaSynThresh = 0.63
	
	
	lemmaResult = {}
	lemmaPosResult = {}
	lemmaSynResult = {}
	
	lemmaSynResultA = {}
	
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
		postags = ["s", "n", "v", "a", "r"]
		for i in range(1, self.data.pairs+1):
			if i % 32 == 0:
				print i*100/800,"%"
			self.data.setCurrentId(i)
			count = 0
			tlemmas = self.data.getTextAttrD("lemma")
			tpos = self.data.getTextAttrD("pos-tag")
			tSlemmas = {}
			for key in tlemmas.keys():
				if tpos.has_key(key):
					tSlemmas[key] = syn.Syn(tlemmas[key], tpos[key].lower()) if tpos[key].lower() in postags else syn.Syn(tlemmas[key])
			
			#print tSlemmas
			hlemmas = self.data.getHypAttrD("lemma")
			hpos = self.data.getHypAttrD("pos-tag")
			hSlemmas = {}
			for key in hlemmas.keys():
				if hpos.has_key(key):
					hSlemmas[key] = syn.Syn(hlemmas[key], hpos[key].lower()) if hpos[key].lower() in postags else syn.Syn(hlemmas[key])
			
			tot = 0
			for key in hlemmas.keys():
				if hlemmas[key] in tlemmas:
					tot += 1
					count += 1
					#print "found xml lemma match"
				else:
					s = hSlemmas[key]
					if len(s.syns) > 0:
						tot += 1
						#print s.syns
						for key2 in tSlemmas.keys():
							t = tSlemmas[key2]
							connection = s.findLemmaConnection(t)
							if connection == 1 or connection == -1:
								count += connection
								break
					
					
					
			self.lemmaSynResult[i] = "YES" if count/tot > self.lemmaSynThresh else "NO"
			self.lemmaSynResultA[i] = count/tot
			#print lemma[i]
		return self.lemmaSynResultA[i]

	# Part IV		
	def matchLemmaSyn2(self):
		lemma = {}
		postags = ["s", "n", "v", "a", "r"]
		for i in range(1, self.data.pairs+1):
			if i % 32 == 0:
				print i*100/800,"%"
			self.data.setCurrentId(i)
			count = 0
			tlemmas = self.data.getTextAttrD("lemma")
			tpos = self.data.getTextAttrD("pos-tag")
			tSlemmas = {}
			for key in tlemmas.keys():
				if tpos.has_key(key):
					tSlemmas[key] = syn.Syn(tlemmas[key], tpos[key].lower()) if tpos[key].lower() in postags else syn.Syn(tlemmas[key])
			
			#print tSlemmas
			hlemmas = self.data.getHypAttrD("lemma")
			hpos = self.data.getHypAttrD("pos-tag")
			hSlemmas = {}
			for key in hlemmas.keys():
				if hpos.has_key(key):
					hSlemmas[key] = syn.Syn(hlemmas[key], hpos[key].lower()) if hpos[key].lower() in postags else syn.Syn(hlemmas[key])
			
			tot = 0
			for key in hlemmas.keys():
				foundKey = False
				for key2 in tlemmas.keys():
					if hlemmas[key] == tlemmas[key2]:
						tot += 1
						count += 1
						#print "found xml lemma match"
						del tlemmas[key2]
						del tSlemmas[key2]
						foundKey = True
						break
					
				if not foundKey:
					s = hSlemmas[key]
					if len(s.syns) > 0:
						tot += 1
						#print s.syns
						for key2 in tSlemmas.keys():
							t = tSlemmas[key2]
							connection = s.findLemmaConnection(t)
							if connection == 1 or connection == -1:
								count += connection
								del tSlemmas[key2]
								del tlemmas[key2]
								break
					
					
					
			self.lemmaSynResult[i] = "YES" if count/tot > self.lemmaSynThresh else "NO"
			self.lemmaSynResultA[i] = count/tot
			#print lemma[i]
		return self.lemmaSynResultA[i]
		
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
		
	def printall(self):
		for i in range(101):
			printer = rp.ResultPrinter(str(i))
			for key in self.lemmaSynResult.keys():
				printer.write(key, "YES" if self.lemmaSynResultA[key] > i/100 else "NO")

if __name__ == "__main__":
	b = OneB()
	#print b.matchLemmaPos()
	b.matchLemmaSyn2()
	b.printall()
