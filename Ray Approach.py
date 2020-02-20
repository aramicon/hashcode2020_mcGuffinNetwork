import sys
import os
from Methods import Methods

switcher = {
    0: Methods.test,
    1: Methods.dumb,
    2: Methods.random,
    3: Methods.greedy,
    4: Methods.flipGreedy,
    5: Methods.knapsolve,
    6: Methods.rebuildHelper,
    7: Methods.solvemc,
	8: Methods.randomTwo
}

dataset = ['a', 'b', 'c', 'd', 'e']

file_switcher = {
    'a': '_example',
    'b': '_read_on',
    'c': '_incunabula',
    'd': '_tough_choices',
    'e': '_libraries_of_the_world'
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

    filein = "data" + seperator + filebase + ".txt"
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

    # Defining output string
    # --------------------------------------------------------

    #finalOutput = " ".join([str(x) for x in resultList])
    finalOutput = resultList["numlibs"] + "\n"
    for lib in resultList["libs"]:
        finalOutput += lib["id"] + " " + lib["numbooks"] + "\n"
        for l in lib["books"]:
            finalOutput += l + " "
        finalOutput += "\n"

    # Printing to file / console
    # --------------------------------------------------------

    fout.write(str(len(resultList)) + "\n")
    fout.write(finalOutput)

    print(resultList)
    print(finalOutput)

    # Close File
    fout.close()


def parseInput(filein):
    # Open File
    fin = open(filein, "r")

    # Parsing Method into data Object
    # ----------------------------------------------


    topline = [int(x) for x in fin.readline().split()]
    print(topline)
    score = [int(x) for x in fin.readline().split()]
    print(score)

    dataset = {
        'numBooks': topline[0],
        'numLibs': topline[1],
        'days': topline[2],
        'scores': score,
        'libs': []
    }

    while True:

        deets = [int(x) for x in fin.readline().split()]
        collection = [int(x) for x in fin.readline().split()]

        if not collection:
            break  # EOF

        dataset['libs'].append({'libBooks': deets[0],
                                'sign': deets[1],
                                'bpd': deets[2],
                                'collection': collection
                                })

    print(dataset)

    # ----------------------------------------------
    # End Parsing, Close file and return data format
    fin.close()
    return dataset


def solutionSolveAll(method):
    for x in dataset:

        dataSetup = setup([x, method])

        func = dataSetup[0]
        data = dataSetup[1]

        resultList = func(data)

        # Outputing reults
        outputResults(dataSetup[2], resultList)


def main():
    runTest = ['b', 0]

    # Setting up function of choice and data to be worked on
    dataSetup = setup(runTest)
    func = dataSetup[0]
    data = dataSetup[1]

    resultList = func(data)

    # Outputing reults
    outputResults(dataSetup[2], resultList)


main()
# solutionSolveAll(7)
