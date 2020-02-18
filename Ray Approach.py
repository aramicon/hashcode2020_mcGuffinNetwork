import sys
import os
from Methods import Methods

switcher = {
    0: Methods.test,
    1: Methods.dumb,
    2: Methods.random,
    3: Methods.greedy
    # 3: Methods.knapsackSolution
}

file_switcher = {
    'a': '_example',
    'b': '_small',
    'c': '_medium',
    'd': '_quite_big',
    'e': '_also_big'
}

seperator = ''
if os.name == "posix":
    seperator = '/'
else:
    seperator = '\\'


def setup(arguments):
    # Choosing which data set and method to use
    # -----------------------------------------
    print()
    lenargs = len(sys.argv)

    if lenargs == 1:
        filebase = arguments[0]
        method = arguments[1]
    elif lenargs == 2:
        filebase = str(sys.argv[1])
        method = 1
    else:
        filebase = str(sys.argv[1])
        method = int(sys.argv[2])

    filebase += str(file_switcher.get(filebase))

    filein = "data" + seperator + filebase + ".in"
    fileout = "data" + seperator + filebase + ".out"

    # Formatting Data and selecting function
    # ----------------------------------------------
    data = parseInput(filein)

    func = switcher.get(method, lambda: "Invalid function")

    return [func, data, fileout]
    # ----------------------------------------------


def outputResults(fileout, resultList):
    # output the results
    fout = open(fileout, "w")
    fout.write(str(len(resultList)) + "\n")
    fout.write(" ".join([str(x) for x in resultList]))
    fout.close()

    print(resultList)


def parseInput(filein):
    # Open File
    fin = open(filein, "r")

    # Parsing Method into data Object
    # ----------------------------------------------

    topline = fin.readline().split()
    maxSize = int(topline[0])
    # numberPizzaShapes = int(topline[1])
    pizzaShapes = [int(x) for x in fin.readline().split()]

    dataFormat = {
        'knapsize': maxSize,
        'pizzas': pizzaShapes
    }

    # ----------------------------------------------
    # End Parsing, Close file and return data format
    fin.close()
    return dataFormat


def main():
    runTest = ['a', 3]

    # Setting up function of choice and data to be worked on
    dataSetup = setup(runTest)
    func = dataSetup[0]
    data = dataSetup[1]

    resultList = func(data)

    # Outputing reults
    outputResults(dataSetup[2], resultList)


main()
