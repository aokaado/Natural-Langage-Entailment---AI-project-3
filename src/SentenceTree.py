import FileReader as fr

class SentenceTree:
	attributes = ["word", "lemma", "pos-tag", "relation"]
	data = 0
	pairs = 0
	idx = 0
	node = 0
	
	def __init__(self):
		xmltree = fr.FileReader("../data/RTE2_dev.preprocessed.xml")
		self.pairs = xmltree.pairs
		self.data = xmltree.elems
		
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
		return [ self.get(self.idx, 0, i, attr) for i in range(0, self.textNodes())]

	def getHypAttr(self, attr):
		return [ self.get(self.idx, 1, i, attr) for i in range(0, self.hypNodes())]
		
