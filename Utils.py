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


    def calculateScore(dataset, resultset):
        #work out the score for a dataset...
        dayOffset = 0
        days=dataset["days"]
        scores = dataset['scores']
        libs = dataset["libs"]
        totalScore = 0
        booksDict = {}
        invalidFlag = False
        for lib in resultset["libs"]:
            originalLib = libs[lib["id"]]
            books = lib["books"]
            bpd = originalLib["bpd"]

            #die121 print("Score library ",lib["id"], ", which has ", len(lib['books']), "books and can process ", originalLib["bpd"], " per day")

            #go from daysOffset to days trying to scan books
            libraryScore = 0
            dayOffset+=originalLib["sign"]
            if days > dayOffset:
                #die121 print("sign-on takes ",originalLib["sign"], " days, offset currently at ", dayOffset, " total days ", days )
                for i in range((days-dayOffset)):
                    #read in a number of books for each day

                    if (i*bpd) < len(books):
                        #die121 print("try to read in books from ", str(i*bpd), " to ", str((i*bpd)+bpd))
                        for k in range(i*bpd,(i*bpd)+bpd):
                            if k < len(books):
                                #if this books was not in the original library, throw a warning/error
                                if books[k] not in originalLib["collection"]:
                                    #die121 print("ERROR, book ",books[k], " is not in the original library ", lib.id)
                                    invalidFlag = True
                                #if this books was already used, ignore it.
                                if books[k] not in booksDict:
                                    #die121 print("adding score of ", scores[books[k]], "for book ", books[k])
                                    libraryScore+= scores[books[k]]
                                    booksDict[books[k]] = 1
                                #else:
                                    #die121 print("Book ", books[k], " was already used, booksDict = ", booksDict)
            #die121 print("Score for library ", lib["id"], " ", libraryScore)
            totalScore+=libraryScore


        if (invalidFlag):
            print("score set to -1 due to invalid flag set")
            totalScore = -1
        #print("Total Score ", totalScore)
        return totalScore
