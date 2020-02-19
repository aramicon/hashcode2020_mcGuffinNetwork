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
		
def randomDumb(maxSize, numberPizzaShapes, pizzaShapes):
	res = set()
	total = 0
	max_score = 0
	best_res = {}
	l = [1,2,3]
	random.shuffle(l)
		
	for att in range(1):
		res = set()
		total = 0
		pizzaShapesShuffledOrder = [x for x in range(numberPizzaShapes)]
		
		random.shuffle(pizzaShapesShuffledOrder)
		#print(pizzaShapesShuffledOrder)
		for i in pizzaShapesShuffledOrder:
			size = pizzaShapes[i]
			if((total + size) <= maxSize):
				total += size
				res.add(i)
		#set best if improved
		if total > max_score:
			max_score = total
			best_res =  res.copy()
			print("found new best score ", max_score)
	print("final score = ",sum([pizzaShapes[p] for p in best_res]))
	print(best_res)
	print(pizzaShapes)
	#for m in best_res:
	#	print("item ",m," is ", pizzaShapes[m])
	return best_res

def randomRefined(maxSize, numberPizzaShapes, pizzaShapes):
	#use the basic random then try to tweak the final set before returning
	basicRandomIndexes = randomDumb(maxSize, numberPizzaShapes, pizzaShapes) #indexes
	pizzaShapes_used = set([pizzaShapes[b] for b in basicRandomIndexes]) #shapes
	print("final score 2= ",sum([pizzaShapes[p] for p in basicRandomIndexes]))
	
	print("pizzaShapes_used ",pizzaShapes_used)
	total = sum(pizzaShapes_used)
	print("total 3 = ",total)
	pizzaShapes_set = set(pizzaShapes)
	pizzaShapes_notUsed = pizzaShapes_set.difference(pizzaShapes_used)
	
	#print("pizzaShapes_notUsed: ",pizzaShapes_notUsed)
	if(pizzaShapes_notUsed):
		pizzaShapes_usedList = SortedList(pizzaShapes_used)
		print("pizzaShapes_usedList", pizzaShapes_usedList)
		
		pizzaShapes_notUsed_list = list(pizzaShapes_notUsed)
		
		#print(pizzaShapes_notUsed_list)
		pizzaShapes_notUsed_list.sort(reverse=True)
		#try to replace items if possible
		for i in pizzaShapes_notUsed_list:
			print("can I use pizza size ", i,"?")
			replace_check = True
			replace_k = 0
			k = len(pizzaShapes_usedList)-1
			print("replace_check ",replace_check, ", k ", k, " len(pizzaShapes_usedList) ", len(pizzaShapes_usedList))
			while(replace_check and k>=0):
				print("k = ",k,",len(shapes)=",len(pizzaShapes_usedList), ". Can I replace ",pizzaShapes_usedList[k]," with ",i," if it puts total to ",((total-pizzaShapes_usedList[k])+i)," and maxSize is ",maxSize,"?")
				
				if i > pizzaShapes_usedList[k]  and (((total-pizzaShapes_usedList[k])+i) <= maxSize):
					replace_check = True
					replace_k = pizzaShapes_usedList[k]
					#replace_check = False
				k-=1
			if replace_k > 0:
				print("can replace ",pizzaShapes_usedList[k]," with ",i," as it puts total to ",((total-pizzaShapes_usedList[k])+i)," and maxSize is ",maxSize,"")
				total = ((total-pizzaShapes_usedList[k])+i)
				pizzaShapes_usedList.discard(k)
				pizzaShapes_usedList.add(i)			
				
	else:
		print("all pizza shapes were used")
		
	res = [pizzaShapes.index(h) for h in pizzaShapes_usedList]
	return basicRandomIndexes


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
		2: randomDumb,
		4: randomRefined
    }
	func = switcher.get(method, lambda: "Invalid function")
	
	resultList = func(maxSize, numberPizzaShapes, pizzaShapes)
	
	#output the results 
	fout = open(fileout,"w")
	fout.write(str(len(resultList)) + "\n")
	print("writing solution to file: ", len(resultList), " pizzas")
	fout.write(" ".join([str(x) for x in resultList]))
	fout.close()
		
	
	
main()


   