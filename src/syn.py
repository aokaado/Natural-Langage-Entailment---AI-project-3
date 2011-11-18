from __future__ import division
from nltk.corpus import wordnet as wn

class Syn:
	syns = None
	lemmas = None
	
	def __init__(self, word, pos = None):
		self.syns = wn.synsets(word)
		if pos:
			self.lemmas = wn.lemmas(word, pos)
			
		
	def __eq__(self, other):
		if self.lemmas and other.lemmas:
			print "NYI"
		else:
			for syn in self.syns:
				if syn in other.syns:
					return True
			return False
