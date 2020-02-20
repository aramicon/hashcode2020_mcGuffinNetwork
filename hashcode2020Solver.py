import sys
import random
from sortedcontainers import SortedList, SortedSet, SortedDict 

def dumb(maxSize, numberPizzaShapes, pizzaShapes):
	res = set()
	total = 0
	for i, size in enumerate(pizzaShapes):
		if((total + size) <= maxSize):
			total += size
			res.add(str(i))
	
	return res
		

def main():

	#*************************INPUT***********************
	lenargs = len(sys.argv)
	
	# example of execution : python hashcode2020Solver.py a 1 #this will run method 1 (mapped to 'dumb' function) on the a data set. all mapppings below.
	file_switcher = {
	'a': '_example',
	'b':'_small',
	'c':'_medium',
	'd':'_quite_big',
	'e':'_also_big'
	}
	print(lenargs)
	
	if lenargs == 1:
		filebase = "a"
		method = 1
	elif lenargs == 2:
		filebase = str(sys.argv[1])
		method = 1
	else:
		filebase = str(sys.argv[1])
		method = int(sys.argv[2])

	filebase += str(file_switcher.get(filebase))
	
	filein = "data\\" + filebase + ".in"
	fileout = "data\\" + filebase + ".out"
	fin = open(filein, "r")
	#get first line 
	topline = fin.readline().split()
	maxSize = int(topline[0])
	numberPizzaShapes = int(topline[1])
	pizzaShapes = [int(x) for x in fin.readline().split()]
	fin.close()
	
	#sort pizza shapes
	pizzaShapes.sort
	print("get as close as possible to ", maxSize, " slices with the ", numberPizzaShapes, "pizza shapes :",  pizzaShapes)
	
	switcher = {
        1: dumb
    }
	func = switcher.get(method, lambda: "Invalid function")
	
	#calls the relevant function
	resultList = func(maxSize, numberPizzaShapes, pizzaShapes)
	
	#*************************OUTPUT*********************** 
	fout = open(fileout,"w")
	fout.write(str(len(resultList)) + "\n")
	print("writing solution to file: ", len(resultList), " pizzas")
	fout.write(" ".join([str(x) for x in resultList]))
	fout.close()
		
	
	
main()


   