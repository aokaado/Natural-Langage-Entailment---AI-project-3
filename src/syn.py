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
	
	def findLemmaConnection(self, other):
		if self.lemmas and other.lemmas:
			for lemma1 in self.lemmas:
				for lemma2 in other.lemmas:
					#if antonym
					if lemma2 in lemma1.antonyms():
						return -1
		
		for syn in self.syns:
			#if synonym
			if syn in other.syns:
				return 1
		#was nothing
		return 0


if __name__ == "__main__":
	good = Syn("good", "a")
	bad = Syn("bad", "a")
	something = Syn("something", "n")
	print good.findLemmaConnection(something)

