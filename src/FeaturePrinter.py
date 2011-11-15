from __future__ import division
from xml.etree.cElementTree import iterparse
import WordMatcher as wm
import lemma_pos as lm
import bleu as bl
import TreeDistance as td

class FeaturePrinter (object):
	
	entailment = None # entailment
	wmf = None # WordMatcher features (weighted)
	lmf = None # LemmaMatcher features
	lpf = None # Lemma-POS features
	b2f = None # Bleu2 Features
	b3f = None # Bleu3 Features
	b4f = None # Bleu4 Features
	tdf = None # Tree-distance features (normalized and weighted)

	def __init__(self):
		self.learnerfile = "../data/RTE2_dev.xml"
		self.learnerfilepp = "../data/RTE2_dev.preprocessed.xml"
		self.wordmatch = wm.WordMatcher(self.learnerfile, True)
		self.lemma = lm.OneB(self.learnerfilepp)
		self.bleu = bl.Bleu(self.learnerfilepp)
		self.tdi = td.TreeDistance(self.learnerfilepp)
		
	def createWMFeatures(self):
		print "creating WMF"
		for i in range(1, len(self.wordmatch.pairs)+1):
			if i % 32 == 0:
				print i*100/800,"%"
			self.wordmatch.match(i)
		self.wmf = self.wordmatch.getFeatures()
	
	def createLFeatures(self):
		print "creating LF"
		self.lmf = self.lemma.matchLemma()

	def createLPFeatures(self):
		print "creating LPF"
		self.lpf = self.lemma.matchLemmaPos()

	def createBleuFeatures(self):
		print "creating BLF"
		self.b2f = self.bleu.getBleu(2)
		self.b3f = self.bleu.getBleu(3)
		self.b4f = self.bleu.getBleu(4)
	
	def createTreeDistFeatures(self):
		print "creating TDF"
		self.tdf = self.tdi.matchTrees(True)
		
	def getEntailments(self):
		print "retrieving entailments"		
		self.entailment = {}
		for event, elem in iterparse(self.learnerfile):
			if elem.tag == "pair":
				self.entailment[elem.get("id")] = elem.get("entailment")
		print self.entailment
				
	def createFeatureFile(self):
		f = open("features.tab", 'w')
		f.write("entailment\twmf\tlmf\tlpf\tb2f\tb3f\tb4f\ttdf\n")
		f.write("d\tc\tc\tc\tc\tc\tc\tc\n")
		f.write("class\t\t\t\t\t\t\t\n")
		
		for i in range(1, len(self.entailment)+1):
			bufferline = self.entailment[str(i)]+"\t"
			bufferline += str(self.wmf[i])+"\t"
			bufferline += str(self.lmf[i])+"\t"
			bufferline += str(self.lpf[i])+"\t"
			bufferline += str(self.b2f[i])+"\t"
			bufferline += str(self.b3f[i])+"\t"
			bufferline += str(self.b4f[i])+"\t"
			bufferline += str(self.tdf[i])+"\n"
			f.write(bufferline)
	
		f.close()	

if __name__ == "__main__":
	featureprinter = FeaturePrinter()
	
	featureprinter.createWMFeatures()
	featureprinter.createLFeatures()
	featureprinter.createLPFeatures()
	featureprinter.createBleuFeatures()
	featureprinter.createTreeDistFeatures()
	
	featureprinter.getEntailments()
	featureprinter.createFeatureFile()
	
	#print len(featureprinter.wmf), len(featureprinter.lmf), len(featureprinter.lpf), len(featureprinter.b2f), len(featureprinter.b3f), len(featureprinter.b4f), len(featureprinter.tdf)
