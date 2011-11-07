class ResultPrinter:
	fp = "../data/results.txt"

	def __init__(self):
		self.f = open(self.fp, 'w')
		self.f.write("ranked: no\n")

	def write(self, idx, res):
		self.f.write(str(idx)+" "+res+"\n")

	def __del__(self):
		self.f.close()		
