class Utils:

    def booksOwned(dataset):
        #print('begining data')

        uniqueness = {}
        for lib in dataset["libs"]:
            for book in lib["collection"]:
                if book not in uniqueness:
                    uniqueness[book] = []
                uniqueness[book].append(lib['id'])


        # print(uniqueness)

        return uniqueness
