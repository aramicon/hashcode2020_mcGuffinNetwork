import random

class Methods:

    def test(input):
        print(input)
        return 'hello world'

    def dumb(maxSize, numberPizzaShapes, pizzaShapes):
        res = set()
        total = 0
        for i, size in enumerate(pizzaShapes):
            if ((total + size) <= maxSize):
                total += size
                res.add(str(i))

        return res

    def random(maxSize, numberPizzaShapes, pizzaShapes):
        res = set()
        total = 0
        max_score = 0
        best_res = {}

        for att in range(100):
            res = {}
            total = 0
            pizzaShapesShuffledOrder = [x for x in range(numberPizzaShapes)]
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

    def greedy(dataset):
        slices = 0
        solution = []
        for i in range(len(dataset['pizzas'])):
            print("Greedy Search " + str(slices + dataset['pizzas'][i]) + " : " + str(dataset['knapsize']))
            if slices + dataset['pizzas'][i] <= dataset['knapsize']:
                slices = slices + dataset['pizzas'][i]
                solution.append(i)
        return solution
