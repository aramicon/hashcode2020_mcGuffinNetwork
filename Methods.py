import random
import progressbar

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

    def random(dataset):
        maxSize = dataset[size]
        pizzaShapes = dataset[dataList]
        res = set()
        total = 0
        max_score = 0
        best_res = {}

        for att in range(100):
            res = {}
            total = 0
            pizzaShapesShuffledOrder = [x for x in range(len(dataset['pizzas']))]
            random.shuffle(pizzaShapesShuffledOrder)
            for i in pizzaShapesShuffledOrder:
                size = pizzaShapes[i]
                if ((total + size) <= maxSize):
                    total += size
                    res.add(str(i))
            # set best if improved
            if total > max_score:
                best_res = res

        return best_res

    def basicH(dataset):
        numBooks = dataset['numBooks']
        days=dataset["days"]
        numLibs = dataset["numLibs"]
        scores = dataset['scores']
        libs = dataset["libs"]

        newlist = sorted(libs, key=lambda x: x.sign)

        res = {}
        res["numLibs"] = numLibs
        resLibDetails = []
        for lib in newlist:
            resLibDetails.append({"id": lib["id"], "numBooks": len(lib["collection"]), "books": [k for k in lib["collection"]]})

        res["libs"] = resLibDetails
        return res

    def flipGreedy(dataset):
        dataset[dataList].reverse()
        output = Methods.greedy(dataset)
        output = [len(dataset[dataList]) - 1 - x for x in output]
        output.reverse()
        return output

    def knapsolve(dataset):
        maxscore = dataset[size]
        dp = [None for _ in range(maxscore + 1)]
        dp[0] = []
        for idx, item in progressbar.progressbar(list(enumerate(dataset[dataList]))):
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
