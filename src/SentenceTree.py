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
	
	def getNodes(self, dataSet, node):
		#subtree = []
		#for node in nodes:
		#print "scanning ", node
		childnodes = []
		for item in dataSet:
			#if item.has_key("parent"): print item["id"], node["id"], item["parent"], item["lemma"] if item.has_key("lemma") else "abstract item"
			if item.has_key("parent") and node["id"] == item["parent"]:
				#print "found item ", item
				childnodes.append(item)
		
		#subtree.append(td.Node( node["lemma"], self.getNodes(dataSet, childnodes)))
		#subtree.append(
		#print childnodes
		lemma = node["lemma"] if node.has_key("lemma") else "ABSTRACT"
		return td.Node( lemma, [self.getNodes(dataSet, cnode) for cnode in childnodes] )
		#print subtree
		#return subtree
				
	def getTextTrees(self):
		textTrees = []
		dataSet = self.data[self.idx][0]
		#print dataSet
		for node in dataSet:
			if not node.has_key("parent"):
				lemma = node["lemma"] if node.has_key("lemma") else "ABSTRACT"
				textTrees.append(td.Node(lemma, self.getNodes(dataSet, node)))
		return td.Node("ROOT", [t for t in textTrees])

	def getHypTrees(self):
		hypTrees = []
		dataSet = self.data[self.idx][1]
		#print dataSet
		for node in dataSet:
			if not node.has_key("parent"):
				lemma = node["lemma"] if node.has_key("lemma") else "ABSTRACT"
				hypTrees.append(td.Node(lemma, self.getNodes(dataSet, node)))
		return td.Node("ROOT", [h for h in hypTrees])
