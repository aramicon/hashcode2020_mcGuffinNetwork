import sys
import random

def dumb(maxSize, numberPizzaShapes, pizzaShapes):
	res = set()
	total = 0
	for i, size in enumerate(pizzaShapes):
		if((total + size) <= maxSize):
			total += size
			res.add(str(i))
	
	return res
		
def random(maxSize, numberPizzaShapes, pizzaShapes):
	res = set()
	total = 0
	max_score = 0
	best_res = {}
	l = [1,2,3]
	random.shuffle(l)
	
	
	for att in range(100):
		res = {}
		total = 0
		pizzaShapesShuffledOrder = [x for x in range(numberPizzaShapes)]
		print(pizzaShapesShuffledOrder)
		random.shuffle(pizzaShapesShuffledOrder)
		for i in pizzaShapesShuffledOrder:
			size = pizzaShapes[i]
			if((total + size) <= maxSize):
				total += size
				res.add(i)
		#set best if improved
		if total > max_score:
			best_res =  res
	
	return best_res


def main():

	lenargs = len(sys.argv)
	
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
	
	#try to get the numbers of slices in a dumb way
	#start with the first pizza that fits and keep adding new pizzas
	
	switcher = {
        1: dumb,
		2: random
    }
	func = switcher.get(method, lambda: "Invalid function")
	
	resultList = func(maxSize, numberPizzaShapes, pizzaShapes)
	
	#output the results 
	fout = open(fileout,"w")
	fout.write(str(len(resultList)) + "\n")
	fout.write(" ".join([str(x) for x in resultList]))
	fout.close()
		
	
	
main()


   