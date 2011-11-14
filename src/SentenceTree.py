from __future__ import division
import FileReader as fr

class SentenceTree:
	attributes = ["word", "lemma", "pos-tag", "relation"]
	data = 0
	pairs = 0
	idx = 0
	node = 0
	df = {}
	
	def __init__(self, abstract = True):
		xmltree = fr.FileReader("../data/RTE2_dev.preprocessed.xml", abstract)
		self.pairs = xmltree.pairs
		self.data = xmltree.elems
		self.texts = None
		
	def get(self, idx, sentence, node, attr):
		node = self.data[idx][sentence][node]
		if node.has_key(attr):
			return node[attr]
		return ""
	
	def setCurrentId(self, idx):
		self.idx = str(idx)

	def textNodes(self):
		return len(self.data[self.idx][0])
		
	def hypNodes(self):
		return len(self.data[self.idx][1])
		
	def getTextAttr(self, attr):
		if attr not in self.attributes:
			print "wrong attribute selected", attr
			exit()
		return [ self.get(self.idx, 0, i, attr) for i in range(0, self.textNodes())]

	def getHypAttr(self, attr):
		if attr not in self.attributes:
			print "wrong attribute selected", attr
			exit()
		return [ self.get(self.idx, 1, i, attr) for i in range(0, self.hypNodes())]
	
	def getNGramText(self, n):
		words = self.getTextAttr("word")
		return [[words[k] for k in range(j, j+n)] for j in range(0, len(words)-n+1)]
		
	def getNGramHyp(self, n):
		words = self.getHypAttr("word")
		return [[words[k] for k in range(j, j+n)] for j in range(0, len(words)-n+1)]
	
	def createCollection(self):
		self.texts = []
		for i in range(1, self.pairs+1):
			self.setCurrentId(i)
			self.texts.append(self.getTextAttr("word"))
			self.texts.append(self.getHypAttr("word"))
			
	def getDf(self, word):
		if not self.df.has_key(word):
			#oldI = self.idx
			if not self.texts:
				self.createCollection()
			#self.idx = oldI
			count = 0
			for text in self.texts:
				if word in text:
					count +=1
			count = 1 if count == 0 else count
			self.df[word] = 1/count
		
		return self.df[word]
			
			
			
			
			
			
