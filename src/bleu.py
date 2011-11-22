from __future__ import division
import SentenceTree as st
import ResultPrinter as rp
import syn

class Bleu:

	thresh = 0.22

	result = {}
	resultw = {}
	
	def __init__(self, learnerfile = "../data/RTE2_dev.preprocessed.xml"):
		# False means exclude abstract nodes
		self.data = st.SentenceTree(learnerfile, False)
		self.bleus = 2
		threshs = [0.22, 0.44, 0.0, 0.0]
		self.thresh = threshs[self.bleus-1]

	def matchBleu(self):
		for n in range(1, self.bleus+1):
			for i in range(1, self.data.pairs+1):
				self.data.setCurrentId(i)
				tBleu = self.data.getNGramText(n)
				hBleu = self.data.getNGramHyp(n)
				count = 0
				for b in hBleu:
					if b in tBleu:
						count += 1
				if n == 1:
				 	self.result[i] = count/len(hBleu)
				else:
					self.result[i] += count/len(hBleu)
		for key in self.result.keys():
			self.resultw[key] = "YES" if self.result[key]/self.bleus > self.thresh else "NO"

	def matchBleuSyn(self):
		for n in range(1, 2+1):
			for i in range(1, self.data.pairs+1):
				if i % 16 == 0:
					print (n-1)*50+i*50/800,"%"
				self.data.setCurrentId(i)
				tBleu = self.data.getNGramText(n)
				hBleu = self.data.getNGramHyp(n)
				if n == 1:
					tSBleu = [syn.Syn(tBleu[t][0]) for t in range(len(tBleu))]
					hSBleu = [syn.Syn(hBleu[t][0]) for t in range(len(hBleu))]
				elif n == 2:
					tSBleu = [[syn.Syn(tBleu[t][0]), syn.Syn(tBleu[t][1])] for t in range(len(tBleu))]
					hSBleu = [[syn.Syn(hBleu[t][0]), syn.Syn(hBleu[t][1])] for t in range(len(hBleu))]
				count = 0
				for k in range(len(hBleu)):
					b = hBleu[k]
					if b in tBleu:
						count += 1
					else:
						b = hSBleu[k]
						for t in tSBleu:
							if n == 1:
								val = b.findLemmaConnection(t)
								if not val == 0:							
									count += val
									break
							else:
								val = b[0].findLemmaConnection(t[0]) * b[1].findLemmaConnection(t[1])
								if not val == 0:
									count += val
									break
				if n == 1:
				 	self.result[i] = count/len(hBleu)
				else:
					self.result[i] += count/len(hBleu)
		for key in self.result.keys():
			self.resultw[key] = "YES" if self.result[key]/2 > self.thresh else "NO"
		
	def getBleu(self, n):
		res = {}
		for i in range(1, self.data.pairs+1):
			self.data.setCurrentId(i)
			tBleu = self.data.getNGramText(n)
			hBleu = self.data.getNGramHyp(n)
			count = 0
			for b in hBleu:
				if b in tBleu:
					count += 1
			res[i] = count/len(hBleu)
		return res
						
	def printResults(self):
		if not self.result:
			self.matchBleu()
		printer = rp.ResultPrinter()
		for key in self.resultw.keys():
			printer.write(key, self.resultw[key])

	def printall(self):
		for i in range(101):
			printer = rp.ResultPrinter(str(i))
			for key in self.result.keys():
				printer.write(key, "YES" if (self.result[key]/self.bleus) > (i/100) else "NO")


if __name__ == "__main__":	
	b = Bleu()
	
	#btestdata = Bleu(learnerfile = "../data/preprocessed-blind-test-data.xml")
	#btestdata.printResults()
	
	#print b.getBleu(2)
	#b.matchBleu()
	b.matchBleuSyn()
	b.printResults()
	b.printall()
