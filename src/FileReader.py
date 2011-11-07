from xml.etree.cElementTree import iterparse

class FileReader:
	fields = ["word", "lemma", "pos-tag", "relation"]	

	def __init__(self, inf):
		self.elems = {}
		self.pairs = 0

		cid = 0
		sentence = []
		attr = {}
		for event, elem in iterparse(inf, events=("start", "end")):

			if event == "start":
				if elem.tag == "pair":
					self.pairs+=1
					cid = elem.get("id")
					self.elems[cid] = []
				elif elem.tag == "node":
					attr = {}
				elif elem.tag == "sentence":
					sentence = []
					
			if event == "end":
				"""
				#end early during testing
				if elem.tag == "pair" and self.pairs > 1:
					break
				"""
				
				if elem.tag == "sentence":
					self.elems[cid].append(sentence)
				elif elem.tag == "node":
					sentence.append(attr)
				elif elem.tag in self.fields:
					attr[elem.tag] = elem.text.strip("\n\t")
					
