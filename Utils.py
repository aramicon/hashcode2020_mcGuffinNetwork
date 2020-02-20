class Utils:

    def listToSet(listIn):
        result = set()

        result.add(x for x in listIn)

        return result

    def sortBySign(dataset):
        libs = dataset['Libs']