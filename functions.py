"""
This module contains all the functions that are used for parsing the expression, creating the expression tree (and converting the input expression to the required form) and the function to create the sim file from the input expression
"""

"""
Working:

Once the input expression is taken, parse the expression and fill it into a tree and implement stack mechanism. Use a similar strategy to evaluation of infix expression
"""

from classes import gate_expression,node_tree

"""
Section of code that contains all functions that are related to parsing the expession
"""

def popnext(input_stream, token):
	if input_stream[0:len(token)] == list(token):
		del input_stream[0:len(token)]
		return True
	return False

def binary_parse(input_stream, operator, nextfn):
	expression_bin = [nextfn(input_stream)]
	while popnext(input_stream, operator):
		expression_bin.append(nextfn(input_stream))
	return '('+'{}'.format(operator).join(expression_bin) + ')' if len(expression_bin) > 1 else expression_bin[0]

def OR_parse(input_stream):
	return binary_parse(input_stream, '+', AND_parse)

def AND_parse(input_stream):
	return binary_parse(input_stream, '.', unary_parse)

def unary_parse(input_stream):
	if popnext(input_stream, '!'):
		return '!{}'.format(unary_parse(input_stream))
	return primary_parse(input_stream)

def primary_parse(input_stream):
	if popnext(input_stream, '('):
		e = OR_parse(input_stream)
		popnext(input_stream, ')')
		return e
	return input_stream.pop(0)

def parse(gate_expression):
	return OR_parse(list(gate_expression.replace(' ', '')))

"""
Section of code that deals with the creation of the expression tree
"""

def tree_create(expression):
	stack=["("]
	expression=expression[1:]
	root=node_tree('')
	while stack and expression: 
		"""
		This part is called after successfully parsing the expression
		"""
		current=expression[0]
		expression=expression[1:]
		if(current.isalpha()):
			"""
			Perform this set of operations when the current in an alphabet i.e. if the current is a gate variable
			"""
			operator=stack[-1]
			if(operator=="!" and root.left==None):
				"""
				If the operator is ! and it is applied to the first gate
				"""
				root.left=node_tree("!",node_tree(current))
			elif(root.left==None):
				"""
				Start building a node and eventually tree, with the first gate as the initial root of the tree
				"""
				root.left=node_tree(current)
			elif(operator in "+."):
				"""
				Switch the gate variables and push them into left and right nodes while root is holding the operator
				"""
				stack.pop()
				root.right=node_tree(current)
				temp=root
				root.value=operator
				root=node_tree('')
				root.left=temp
			elif(operator=="!"):
				"""
				Left will hold the gate while the right holds the ! operator
				"""
				stack.pop()
				root.value=stack.pop()
				root.right=node_tree("!",node_tree(current))
				temp=root
				root=node_tree('')
				root.left=temp
		elif current in ".+!":
			"""
			If the current is an operator then append the operator to the stack
			"""
			stack.append(current)
		elif(current=="("):
			"""
			If the current is beginning a new set of braces then create a new tree
			For the set of operators and current position, follow the same rules as above
			"""
			operator=stack[-1]
			count,ind=1,0
			for i in range(0,len(expression)):
				if(expression[i]=="("):
					count+=1
				elif(expression[i]==")"):
					count-=1
					if(count==0):
						ind=i
						break
			new="("+expression[0:ind+1]
			expression=expression[ind+1:]
			if(operator=="!" and root.left==None):
				root.left=node_tree("!",tree_create(new))
			elif(root.left==None):
				root.left=tree_create(new)
			elif(operator in "+."):
				root.right=tree_create(new)
				temp=root
				root.value=stack.pop()
				root=node_tree('')
				root.left=temp
			elif(operator=="!"):
				stack.pop()
				root.right=node_tree("!",tree_create(new))
				temp=root
				root.value=stack.pop()
				root=node_tree('')
				root.left=temp
		elif(current==")"):
			stack.pop()
			"""
			When the current is ) i.e. end of that expression block, then pop the stack
			"""
	if(root.value==''):
		return root.left
		"""
		Return the left child if the root is empty
		"""
	return root

def sim_file_creator(expression,filename):
	expression="(%s)"%parse("(%s)"%expression)
	"""
	Parse the input expression given and then create a tree with that input expression
	"""
	root=tree_create(expression)
	
	root.print();

	sim_file=open(filename,"w")
	"""
	Open a sim file and start writing the required contents into the file
	"""
	sim_file.write("| boolean gate_expression is %s\n\n"%expression[1:-1])
	sim_file.write("| type gate source drain length width\n| ------------------------------\n")
	"""
	Calling the sim_file_extract function from classes to evaluate the expression and choose the proper contents of each variable/gate in the expression
	"""
	root.sim_file_extract(sim_file)
	"""
	Close the file after writing
	"""
	sim_file.close()
