#!/usr/bin/env python
# -*- coding: utf-8 -*-

#*************************************************************************
#
#	 This sample implementation is incomplete!
#	 You need to implement the remaining parts yourself.
#
#*************************************************************************
	
"""
Sample implementation of tree edit distance algorithm from 
Kaizhong Zhang & Dennis ShaSha, 
"Simple fast algorithms for the editing distance beteen trees and related problems",
SIAM Journal on Computing, Vol. 18, No. 6, pp. 1245-1262, 1989.

This is a fairly literal translation of the algorithm described in the paper.
It can probably be improved in several ways, e.g., by avoiding recursion in
the preprocessing.
"""

# EM - 11/2011
insertion_cost = 1
deletion_cost = 1
substition_cost = 1

class Node(list):
	"""
	Simple recursive representation of a tree as a labeled node with zero or
	more child nodes
	"""

	def __init__(self, label, *children):
		self.label = label
		if len(children) == 1 and isinstance(children, (list, tuple)):
			children = children[0]
		list.__init__(self, children)
		
	def is_leaf(self):
		return not self
	
	def left_child(self):
		return self[0]

	def __str__(self):
		"""
		string representation of tree as a labeled bracket structure
		"""
		if self.is_leaf():
			return self.label
		else:
			return ( self.label + 
					 "( " + 
					 " ".join([str(child) for child in self]) + 
					 ")" )
		
	def __repr__(self):
		return self.label
		
	
class ForestDist(dict):
	"""
	ForestDist is a dictionary storing the distance between two forest.

	Keys are tuples of the form (forest1, forest2)

	forest1 is either a tuple (i1,j2) where
	i1 = start index of source forest1 and
	j1 = end index of source forest1,
	or None (i.e. empty forest)
	
	Likewise forest2 is eitehr a tuple (i2,j2) where 
	i2 = start index of target forest2 and
	j2 = end index of target forest2,
	or None (i.e. empty forest).
	
	Values are distances >= 0.
	
	By definition, 
	ForestDist(None,None) = 0 and
	forest (i,j) = None when i>j.
	"""
	
	def __init__(self,*args, **kwargs):
		dict.__init__(self, *args, **kwargs)
		# forestdist(Ø,Ø) = 0
		# (cf. Zhang & Shasha:p.1253)
		self[None,None] = 0
		
	def __getitem__(self, (forest1, forest2)):
		# If i>j, then T[i..j] = 0
		# (cf. Zhang & Shasha:p.1249)
		if forest1 is not None:
			i1, j1 = forest1
			if i1 > j1:
				forest1 = None
				
		if forest2 is not None:
			i2, j2 = forest2
			if i2 > j2:
				forest2 = None
				
		return dict.__getitem__(self, (forest1, forest2))
				
		
		
def unit_costs(node1, node2):
	"""
	Defines unit cost for edit operation on pair of nodes,
	i.e. cost of insertion, deletion, substitution are all 1
	"""
	# insertion cost
	if node1 is None:
		return insertion_cost
	
	# deletion cost
	if node2 is None:
		return deletion_cost
	
	# substitution cost
	if node1.label != node2.label:
		return substition_cost
	else:
		return 0

	
def postorder(root_node):
	"""
	Return a list of nodes resulting from a left-to-right postorder traversal
	of the tree rooted in root_node
	"""
	# Cf.  Zhang & Shasha:p.1249:
	# "Let T[I] be the ith node in the tree according to the left-to-right
	# postordering"

	#*************************************************************************
	#
	#	 Your implementation goes here
	#
		
	if root_node.is_leaf():
		return [root_node]
	node = root_node
	stack = []
	
	def buildpost(node, stack):
		if not node.is_leaf():
			for nodec in node:
				buildpost(nodec, stack)
				stack.append(nodec)
	buildpost(node, stack)
	stack.append(root_node)
	#print stack
	return stack
	
	#
	#
	#
	#*************************************************************************
	
	
def leftmost_leaf_descendant_indices(node_list):
	"""
	Return a list of the *indices* of the leftmost leaf descendants according
	to a list of post-ordered nodes
	"""
	# Cf.  Zhang & Shasha:p.1249:
	# "l(i) is the number of the leftmost leaf descendant of the subtree
	# rooted at T[i]. When T[i] is a leaft, l(i)=i."


	#*************************************************************************
	#
	#	Your implementation goes here
	#
		
	indice_list = []
	for i in range(0, len(node_list)):
		node_list[i].label = node_list[i].label+"X"+str(i)
	for node in node_list:
		cnode = node
		while not cnode.is_leaf():
			cnode = cnode.left_child()
		
		# this does not work? says every leaf node is idx 0
		#indice_list.append(node_list.index(cnode))
		for i in range(0, len(node_list)):
			#node_list[i] == cnode is dubious.....
			if str(node_list[i]) == str(cnode):
				indice_list.append(i)
				#print "found ", str(cnode), " at ", i
	#print node_list
	for i in range(0, len(node_list)):
		node_list[i].label = node_list[i].label.split("X")[0]
	#print node_list
	#print len(node_list), len(indice_list), indice_list
	return indice_list

	#
	#
	#
	#*************************************************************************
		
		
		
def key_root_indices(lld_indices):
	"""
	Return a list of the *indices* of the key roots from a list of the indices
	of the leftmost leaf descendants
	"""
	# Cf. Zhang & Shasha:p.1251: "LR_keyroots(T) = {k| there exists no k'>k
	# such that l(k)=l(k')}
	
	
	#*************************************************************************
	#
	#	Your implementation goes here
	#
	
	key_roots = []
	helper = []
	for idx in range(len(lld_indices)-1, -1, -1):
		if not lld_indices[idx] in helper:
			key_roots.append(idx)
			helper.append(lld_indices[idx])
	key_roots.reverse()

	return key_roots
	#
	#
	#
	#*************************************************************************
	
	
	
def distance(t1, t2, costs=unit_costs):
	"""
	Compute edit distance between tree t1 and tree t2
	Unit costs are used if no explicit costs are provided.
	"""
	# Cf. Zhang & Shasha:p.1252-1253

	# Use an embedded function, so T1,T2, l1,l2, and TD are available from the
	# name space of the outer function and don't need to be dragged around in
	# each function call
	def edit_dist(i, j):
		"""
		compute edit distance between two subtrees rooted in nodes i and j
		respectively
		"""
		# temporary array for forest distances
		FD = ForestDist()
		for n in range(l1[i], i+1):
			FD[ (l1[i],n), None ] = ( FD[ (l1[i],n-1), None ] + 
									  costs(T1[n], None) )
			
		for m in range(l2[j], j+1):
			FD[ None, (l2[j],m) ] = ( FD[ None, (l2[j],m-1) ] + 
									  costs(None, T2[m]) )
			
		
		#*************************************************************************
		#
		#	Your implementation of the final part of edit_dist goes here
		#
		for n in range(l1[i], i+1):
			for m in range(l2[j], j+1):
				if l1[n] == l1[i] and l2[m] == l2[j]:
					FD[ (l1[i],n) , (l2[j], m) ] = min( 
						min( 
							FD[ (l1[i],n-1) , (l2[j], m) ] + costs(T1[n], None) , 
							FD[ (l1[i],n) , (l2[j], m-1) ] + costs(None, T2[m]) 
							) ,
						FD[ (l1[i],n-1) , (l2[j], m-1) ] + costs(T1[n], T2[m])
						)
					TD[n,m] = FD[ (l1[i],n) , (l2[j], m) ]
				else:
					FD[ (l1[i],n) , (l2[j], m) ] = min(
						min(
							FD[ (l1[i],n-1) , (l2[j], m) ] + costs(T1[n], None) , 
							FD[ (l1[i],n) , (l2[j], m-1) ] + costs(None, T2[m]) 
							) ,
							FD[ (l1[i],l1[n]-1) , (l2[j], l2[m]-1) ] + TD[n,m]
						)
		#
		#
		#
		#*************************************************************************
		
		return TD[i,j]
	
	
	# Compute T1[] and T2[]
	T1 = postorder(t1)
	T2 = postorder(t2)
	
	# Compute l()
	l1 = leftmost_leaf_descendant_indices(T1)
	l2 = leftmost_leaf_descendant_indices(T2)
	
	# LR_keyroots1 and LR_keyroots2
	kr1 = key_root_indices(l1)
	kr2 = key_root_indices(l2)
	# permanent treedist array
	TD = dict()

	for i in kr1:
		for j in kr2:
			edit_dist(i, j)
	
	#print_matrix(T1, T2, TD)
	
	return TD[i,j]
			
	
		
def print_matrix(T1, T2, TD):
	print "   " + "".join([("%-3s" % n.label) for n in T2])
	for i in range(len(T1)):
		print "%-2s" % T1[i].label,
		for j in range(len(T2)):
			print "%-2s" % TD[i,j],
		print
	print

	

if __name__ == "__main__":
	# Cf. Zhang & Shasha: Fig. 4 and Fig. 8
	print "a"
	t1 = Node("f",
			Node("d",
				Node("a"),
				Node("c", Node("b") , Node("k"), Node("r")) 
				),
			Node("e"))
	
	t2 = Node("f",
			Node("c",
				Node("d",
					Node("a"),
					Node("b"))),
			Node("e"))

	print "t1 =", t1	
	print "t2 =", t2
	print
	
	d = distance(t1, t2) 
	print "distance =", d


