"""
Design Activity-1

Code to generate a sim file after getting the input of a gate expression

Convert a gate expression into a CMOS layout

Written by Thigulla Vamsi Krishna, COE18B056
"""
"""
Run python3 generator.py to execute the code.
Use irsim to test the working of .sim file
"""
from functions import sim_file_creator

"""
This code module is used to take inputs from the user and generate the sim file
"""


if __name__ == "__main__":
	print("Welcome to sim file generator. Use:\n.  for logical AND\n+ for logical OR\n! for logical NOT\n() for braces\nOnly single character labelled variables(gates)\n")
	exp=input("Enter the gate expression: ")
	filename=input("Enter the output filename(along with extension): ")
	sim_file_creator(exp,filename)
	print("\n%s created successfully"%filename)
	"""
	Section to simply display the .sim file output for user to check
	"""
	sim_file=open(filename,"r")
	for line in sim_file:
		print(line)
	sim_file.close()
