from __future__ import division
import FileReader as fr
import treeEdit as td

class SentenceTree:
	attributes = ["word", "lemma", "pos-tag", "relation", "parent", "id"]
	data = 0
	pairs = 0
	idx = 0
	node = 0
	df = {}
	
	def __init__(self, inputfile = "../data/RTE2_dev.preprocessed.xml", abstract = True):
		xmltree = fr.FileReader(inputfile, abstract)
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
	
	def getTextAttrD(self, attr):
		res = {}
		if attr not in self.attributes:
			print "wrong attribute selected", attr
			exit()

		for i in range(0, self.textNodes()):
			res[i] = self.get(self.idx, 0, i, attr)
		return res
		
	def getHypAttrD(self, attr):
		res = {}
		if attr not in self.attributes:
			print "wrong attribute selected", attr
			exit()
		for i in range(0, self.hypNodes()):
			res[i] = self.get(self.idx, 1, i, attr)
		return res
	
	def getNGramText(self, n):
		words = self.getTextAttr("lemma")
		return [[words[k] for k in range(j, j+n)] for j in range(0, len(words)-n+1)]
		
	def getNGramHyp(self, n):
		words = self.getHypAttr("lemma")
		return [[words[k] for k in range(j, j+n)] for j in range(0, len(words)-n+1)]
	
	def createCollection(self, attr):
		self.texts = []
		for i in range(1, self.pairs+1):
			self.setCurrentId(i)
			self.texts.append(self.getTextAttr(attr))
			self.texts.append(self.getHypAttr(attr))
			
	def getDf(self, word, attr = "word"):
		if not self.df.has_key(word):
			#oldI = self.idx
			if not self.texts:
				self.createCollection(attr)
			#self.idx = oldI
			count = 0
			for text in self.texts:
				if word in text:
					count +=1
			count = 1 if count == 0 else count
			self.df[word] = 1/count
		
		return self.df[word]
	
	def getNodes(self, dataSet, node):
		childnodes = []
		for item in dataSet:
			if item.has_key("parent") and node["id"] == item["parent"]:
				childnodes.append(item)
		
		lemma = node["lemma"] if node.has_key("lemma") else "ABSTRACT"
		#try:
		return td.Node( lemma, [self.getNodes(dataSet, cnode) for cnode in childnodes] )
		"""
		except RuntimeError:
			print self.idx
			print dataSet
			print node
			exit()
			#return td.Node("EXCEPTION")
		"""
				
	def getTextTree(self):
		textTrees = []
		dataSet = self.data[self.idx][0]
		for node in dataSet:
			if not node.has_key("parent"):
				lemma = node["lemma"] if node.has_key("lemma") else "ABSTRACT"
				textTrees.append(td.Node(lemma, self.getNodes(dataSet, node)))
		return td.Node("ROOT", [t for t in textTrees])

	def getHypTree(self):
		hypTrees = []
		dataSet = self.data[self.idx][1]
		#print dataSet
		for node in dataSet:
			if not node.has_key("parent"):
				lemma = node["lemma"] if node.has_key("lemma") else "ABSTRACT"
				hypTrees.append(td.Node(lemma, self.getNodes(dataSet, node)))
		return td.Node("ROOT", [h for h in hypTrees])
