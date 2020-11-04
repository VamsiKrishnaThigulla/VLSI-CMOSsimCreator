"""
This module contains all the various classes used for evaluating the gate expression and making the sim file for the expression
The respective functions for the classes, used to make the sim file and to convert the expression are also in the classes
"""

class gate_expression:
	"""
	Constructors to initialize the class object
	"""
	def __init__(self,operator,operand_1,operand_2=''):
		self.operand_1=operand_1
		self.operand_2=operand_2
		self.operator=operator

	def __str__(self):
		return self.operand_1+self.operator+self.operand_2

	def sim_createfile(self,out):
		"""
		Function to evaluate the expression and decide the content of the file to be written for each specific gate expresion
		"""
		if(self.operator=='!'):
			return "p %s vdd %s 2 4\nn %s gnd %s 2 4\n\n"%(self.operand_1,out,self.operand_1,out)
		elif(self.operator=='+'):
			intermediary=self.operand_1+"_nor_"+self.operand_2+"_int" 
			"""
			Use an intermediary expression which acts as a wire between two gates in serial
			+ operator can be converted into NOR which will acts as serial on p type and parallel on n tpye
			"""
			p1="p %s %s %s 2 4\n"%(self.operand_1,"vdd",intermediary)
			p2="p %s %s %s 2 4\n"%(self.operand_2,intermediary,out)
			n1="n %s %s %s 2 4\n"%(self.operand_1,out,"gnd")
			n2="n %s %s %s 2 4\n\n"%(self.operand_2,out,"gnd")
			return p1+p2+n1+n2
		elif(self.operator=='.'):
			intermediary=self.operand_1+"_nand_"+self.operand_2+"_int"
			"""
			Use an intermediary expression which acts as a wire between two gates in serial
			. operator can be converted into NAND which will acts as parallel on p type and serial on n tpye
			"""
			p1="p %s %s %s 2 4\n"%(self.operand_1,"vdd",out)
			p2="p %s %s %s 2 4\n"%(self.operand_2,"vdd",out)
			n1="n %s %s %s 2 4\n"%(self.operand_1,out,intermediary)
			n2="n %s %s %s 2 4\n\n"%(self.operand_2,intermediary,"gnd")
			return p1+p2+n1+n2
		"""
		Return the expression that is to be written into the file
		"""

class node_tree:
	
	def __init__(self,value,left=None,right=None):
		self.value=value
		self.left=left
		self.right=right

	def print(self,l=0):
		if(self.right!=None):
			self.right.print(l+1)      
		print()
		print("   "*l,end="")
		print(self.value)
		if(self.left!=None):
			self.left.print(l+1) 

	def sim_file_extract(self,sim_file,id=0,inversion=1):
		"""
		Function to evaluate the expression, and store the content (content to be written for each gate) into the sim file according to the rules specified above
		"""
		if(self.value not in "+.!"):
			return self.value

		out="out_%s"%id
		if(self.value=="!"):
			if(self.left.left==None):
				if(id==0):
					out="out"
				expression=gate_expression("!",self.left.value)
				sim_file.write(expression.sim_createfile(out))
				return out
			else:
				if(id!=0):
					id+=1
				left_out=self.left.sim_file_extract(sim_file,id,0)
				return left_out
		else:
			left_out=self.left.sim_file_extract(sim_file,id+1)
			right_out=self.right.sim_file_extract(sim_file,id+2)
			expression=gate_expression(self.value,left_out,right_out)
			if(out=="out_0" and not inversion):
				out="out"
			sim_file.write(expression.sim_createfile(out))
			if(inversion):
				expression=gate_expression("!",out)
				if(out=="out_0"):
					out="out"
				else:
					out=out+"_o"
				sim_file.write(expression.sim_createfile(out))
			return out
