import random
import copy 
#import progressbar
from Utils import Utils

dataList = "pizzas"
size = "knapsize"

class Methods:

    def score(solution, dataset):
        res = 0
        for idx in solution:
            res += dataset['pizzas'][idx]
        return 0 if res > dataset['knapsize'] else res

    def test(dataset):
        print(input)
        return 'hello world'

    def dumb(dataset):
        numBooks = dataset['numBooks']
        days=dataset["days"]
        numLibs = dataset["numLibs"]
        scores = dataset['scores']
        libs = dataset["libs"]


        res = {}
        res["numLibs"] = numLibs
        resLibDetails = []
        for i, lib in enumerate(libs):
            resLibDetails.append({"id": i, "numBooks": len(lib["collection"]), "books": [k for k in lib["collection"]]})

        res["libs"] = resLibDetails



        return res

    def roundR(dataset):
        maxSize = dataset[size]
        pizzaShapes = dataset[dataList]
        res = set()
        total = 0
        max_score = 0
        best_res = {}

        bpl = int(dataset['numBooks']/dataset['numLibs'])

        # print(bpl)

        result = {
            "numLibs": dataset['numLibs'],
            "libs": []
        }

        libraries = dataset["libs"]
        for lib in libraries:
            collection = []
            for bk in range(bpl):
                if(len(lib['collection'])<=bk):
                    break
                collection.append(lib['collection'][bk])

            libOut = {
                "id": lib["id"],
                "numBooks": bpl,
                "books": collection
            }
            result['libs'].append(libOut)

        print(result)
        #
        return result

    def basicH(dataset, weightings={},calculateScore=True):
        #print("you basic")
        numBooks = dataset['numBooks']
        days=dataset["days"]
        numLibs = dataset["numLibs"]
        scores = dataset['scores']
        libs = dataset["libs"]

        #add a new attribute to include the average score per book of a library
        maxSignOnDelay = 0
        maxBookAverageScore = 0
        maxBooksPerDay = 0
        maxCollectionSize = 0

        for l in libs:
            if (l["sign"] > maxSignOnDelay):
                maxSignOnDelay =l["sign"]
            l["averageBookScore"] = (sum([scores[x] for x in l["collection"]])/l["libBooks"])

            if (l["averageBookScore"] > maxBookAverageScore):
                maxBookAverageScore=l["averageBookScore"]
            if (len(l["collection"]) > maxCollectionSize):
                maxCollectionSize+=len(l["collection"])
            if (l["bpd"] > maxBooksPerDay):
                maxBooksPerDay+=l["bpd"]


        #add some weightings for the signon offset, the collection size, and the avg. book value
        #print("maxSignOnDelay ",maxSignOnDelay,"maxBookAverageScore ",maxBookAverageScore,"maxBooksPerDay ",maxBooksPerDay,"maxCollectionSize ",maxCollectionSize)

        BookAverageScoreWeight = 1.0
        SignOnDelayWeight = 4.0
        CollectionSizeWeight = 4.0
        BooksPerDayWeight = 0.0

        

        if 'BookAverageScoreWeight' in weightings:
            BookAverageScoreWeight = float(weightings["BookAverageScoreWeight"])
        if 'SignOnDelayWeight' in weightings:
            SignOnDelayWeight = float(weightings["SignOnDelayWeight"])
        if 'CollectionSizeWeight' in weightings:
            CollectionSizeWeight = float(weightings["CollectionSizeWeight"])
        if 'BooksPerDayWeight' in weightings:
            BooksPerDayWeight = float(weightings["BooksPerDayWeight"])
        #print("libs in method: ", libs)
        print(BookAverageScoreWeight,"/",SignOnDelayWeight,"/",CollectionSizeWeight,"/",BooksPerDayWeight,end="")
        for l in libs:
            #print("l: ",l)
            l["sortweight"] = (((l["averageBookScore"]/maxBookAverageScore)*BookAverageScoreWeight)+ (( (1-(l["sign"]/maxSignOnDelay))*SignOnDelayWeight))+ ((len(l["collection"])/maxCollectionSize)*CollectionSizeWeight)+ ((l["bpd"]/maxBooksPerDay)*BooksPerDayWeight))
            #print("lib ", l["id"], " ", l["sortweight"])

        #sort by delay so you start using the first lib ready
        newlist = sorted(libs, key=lambda l: l["sortweight"],reverse=True)

        #print(newlist)

        #take out book duplicates
        alreadyUsed = {}
        for i,lib in enumerate(newlist):
            for book in lib["collection"]:
                if book in alreadyUsed:
                    #randomly remove book from either current lib or lib in dict :-)
                    #if random.randint(1,2) == 1:
                    lib["collection"].remove(book)
                    #else:
                    #newlist[alreadyUsed[book]]["collection"].remove(book)
                    #alreadyUsed[book] = i
                else:
                    alreadyUsed[book] = i
            #also sort the books by score desc so the high ones get done first
            lib["collection"] = sorted(lib["collection"], key=lambda b: scores[b],reverse=True)

        #remove any empty libraries?
        noItems = [i for i,x in enumerate(newlist) if len(x["collection"]) == 0]
        #print("alreadyUsed: ",alreadyUsed)
        #print("found ", str(len(noItems)), " empty libraries")
        #seems to be none.
        #if len(noItems) > 0:
            #remove them
            #for l in noItems:
            #    newlist.pop(l)

        #print("sorted list with lambda")
        res = {}


        numLibsC = 0
        resLibDetails = []
        #print("add to results object")
        for lib in newlist:
            if(len(lib["collection"]) > 0):
                numLibsC+=1
                resLibDetails.append({"id": lib["id"], "numBooks": len(lib["collection"]), "books": [k for k in lib["collection"]]})
        res["numLibs"] = numLibsC
        res["libs"] = resLibDetails
        #print("return results")

        #work out the projected score: can use this as a fitness function
        if(calculateScore):
            cs = Utils.calculateScore(dataset, res)
            print("Using BookAverageScoreWeight " + str(BookAverageScoreWeight) + " SignOnDelayWeight " + str(SignOnDelayWeight) + " CollectionSizeWeight " + str(CollectionSizeWeight) + " BooksPerDayWeight " + str(BooksPerDayWeight) + "::: " + str(cs))
            res["calculatedScore"] = Utils.calculateScore(dataset, res)
        return res





    def basicHVaryWeights(dataset):
        print("try to find best combination of weights for dataset")
        BookAverageScoreWeightSet = [0]
        SignOnDelayWeightSet = [0]
        CollectionSizeWeightSet = [0,1,1.2,1.4,1.6]
        BooksPerDayWeightSet = [0]
        


        bestScore = 0
        bestScoreResult = {}
        best_i=-5
        best_j=-5
        best_k=-5
        best_l=-5
     

        for i in BookAverageScoreWeightSet:
            for j in SignOnDelayWeightSet:
                for k in CollectionSizeWeightSet:
                    for l in BooksPerDayWeightSet:                      
                        res = Methods.basicH(copy.deepcopy(dataset), weightings={"BookAverageScoreWeight":i,"SignOnDelayWeight":j,"CollectionSizeWeight":k,"BooksPerDayWeight":l},calculateScore=True)
                      
                        print(" i ", i, "j ", j, " k ", k, " l ", l, " : ", str(res["calculatedScore"]))
                        if res["calculatedScore"] > bestScore:
                            bestScore = res["calculatedScore"]
                            bestScoreResult = res
                            best_i=i
                            best_j=j
                            best_k=k
                            best_l=l
        print("** Found best score of " + str(bestScore) + " with values i " + str(best_i) + " j " + str(best_j) + " k " + str(best_k) + " l " + str(best_l) + " m " + "**")
        
        return bestScoreResult

    def knapsolve(dataset):
        maxscore = dataset[size]
        dp = [None for _ in range(maxscore + 1)]
        dp[0] = []
        for idx, item in (list(enumerate(dataset[dataList]))):
            for i in range(maxscore - item, -1, -1):
                if dp[i] is None: continue
                dp[i + item] = dp[i] + [idx]
        i = -1
        while dp[i] is None:
            i -= 1

        return dp[i]

    def rebuildHelper(dataset):
        temp = Methods.flipGreedy(dataset)
        return Methods.rebuild(temp, dataset)

    def rebuild(solution, dataset):
        newsol = list(solution)
        for i in range(min(len(newsol), 3)):
            idx = random.randrange(len(newsol))
            print(idx, dataset[dataList][newsol[idx]])
            del newsol[idx]
        newscore = Methods.score(newsol, dataset)
        remaining = dataset[size] - newscore
        st = set(newsol)
        newpizz = []
        for i in range(len(dataset[dataList])):
            if i in st:
                # Pizzas already used in the solution are replaced with infinite slices
                # so we avoid selecting them twice while keeping the list indices correct
                newpizz.append(99 ** 99)
            else:
                newpizz.append(dataset[dataList][i])
        print('rem', remaining)
        reco = Methods.knapsolve({dataList: newpizz, size: remaining})
        return sorted(newsol + reco)

    def solvemc(dataset):
        capa = dataset[size]
        sol = []
        for i in range(len(dataset[dataList]) - 1, -1, -1):
            if random.getrandbits(2) and capa >= dataset[dataList][i]:
                sol.append(i)
                capa -= dataset[dataList][i]
        st = set(sol)
        for i in range(len(dataset[dataList]) - 1, -1, -1):
            if i not in st and capa >= dataset[dataList][i]:
                sol.append(i)
                capa -= dataset[dataList][i]
        return sol

    def randomTwo(dataset):
        numberPizzaShapes = len(dataset['pizzas'])
        maxSize = dataset['knapsize']
        pizzaShapes = dataset['pizzas']
        res = set()
        total = 0
        max_score = 0
        best_res = {}
        l = [1,2,3]
        random.shuffle(l)

        for att in range(1000):
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
        #    print("item ",m," is ", pizzaShapes[m])
        return best_res
