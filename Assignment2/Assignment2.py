import time
from collections import deque
from operator import itemgetter

class Scroggle(object):

    def __init__(self):
        self.dimen=0
        self.frontier=deque()
        self.board=[]
        self.numQueries=0
        self.dict=set()
        self.numWordsWithPrefix = {}
        self.averageWordScore = {}
        self.avgNumLettersAfterPrefix = {}
        self.letterWeights = []
        self.constants = {}

    # @brief    Takes a file name and makes it usable
    # @parem[in]    boardFile
    #               String containing the name of a text file with the board
    def importBoard(self, boardFile):
        with open(boardFile) as f:
            for xindex, line in enumerate(f, start=0):
                letters=line.split()
                for yindex, char in enumerate(letters, start=0):
                    self.board.append(char.lower())
            self.dimen=xindex+1

    # @brief    If the word has a 'qu' we handle it here
    # @details  As per the instructions, a board with the word 'queen'
    #           should be translated as 'qeen'.  If there is a naturall
    #           occurance of 'queen' with the 'u', I treat this as a word
    #           as well so in the master dictionary, 'queen' and 'qeen' occur
    # @parem[in]    word
    #               The string with a occurance of 'qu'
    def handleQU(self, word):
        stringWithU = ""
        stringWithoutU = ""
        for letter in word:
            if stringWithU=="":
                stringWithU+=letter
                stringWithoutU += letter
            elif stringWithU[-1]=="q" and letter=="u":
                stringWithU += letter
                continue
            else:
                stringWithoutU+=letter
            self.addTo_numWordsWithPrefix(stringWithU)
            self.addTo_numWordsWithPrefix(stringWithoutU)

    def addTo_numWordsWithPrefix(self, word):
        try:
            self.numWordsWithPrefix[word] += 1
        except KeyError:
            self.numWordsWithPrefix[word] = 1


    # @brief    Takes the name of the dictionary file and imports it
    # @details  Here we go through the dictionary file and analyze each word
    #           adding every possible prefix and the number of occurances to
    #           numWordsWithPrefix.  There are two more dictionaries with the
    #           same domain (ie all possible prefixes). Instead of counting
    #           pure occurances, averageWordScore stores the average word score
    #           that that prefix will produce if expanded and avgNumLettersAfterPrefix
    #           stores the average number of letters that can be expected after the prefix ends
    # @parem[in]    dictFile
    #               String containing the name of a text file with a dictionary
    def importDictionary(self, dictFile):
        startTime = time.perf_counter()
        lastLine=""
        prefix = ""
        wordScore = 0
        oldAverage = 0
        oldNumPrefixes = 0
        newAverage = 0
        with open(dictFile) as f:
            for word in f:
                word = word[:-1]
                lastline=word
                wordScore = self.getWordScore(word)

                if "qu" in word:
                    self.handleQU(word)

                for i in range(len(word)):
                    if i==(len(word)-1):
                        self.dict.add(word)
                        try:
                            self.numWordsWithPrefix[word] += 1
                        except KeyError:
                            self.numWordsWithPrefix[word] = 1
                    else:
                        prefix = word[:i + 1]
                        #   If the prefix has already been encounteres
                        try:
                            oldAverage = self.averageWordScore[prefix]
                            oldNumPrefixes = self.numWordsWithPrefix[prefix]
                            newAverage = (oldAverage + wordScore)/(oldNumPrefixes+1)
                            self.averageWordScore[prefix] = newAverage
                            self.numWordsWithPrefix[prefix] += 1

                            oldAverage = self.avgNumLettersAfterPrefix[prefix]
                            newAverage = (oldAverage + len(word))/(oldNumPrefixes+1)
                            self.avgNumLettersAfterPrefix[prefix] = newAverage
                        #   If the prefix is new
                        except KeyError:
                            self.numWordsWithPrefix[prefix] = 1
                            self.averageWordScore[prefix] = wordScore
                            self.avgNumLettersAfterPrefix[prefix] = len(word)
        self.dict.add(lastline)
        self.addTo_numWordsWithPrefix(lastline)
        print("Time to import dictionaries: ", time.perf_counter() - startTime)

    # @brief    Converts a word into its total point value
    # @parem[in]    word
    #               A string containing a word with only lowercase letters
    # @parem[out]   An int with the score of the inputted word
    def getWordScore(self, word):
        wordScore = 0
        for char in word:
            wordScore += self.letterWeights[ord(char) - ord('a')]
        return wordScore

    # @brief    Takes a file with lines in this format: "X 0"
    # @parem[in]    weightPath
    #               A String containing the name of a text file with weights
    def importWeights(self, weightPath):
        with open(weightPath) as f:
            for line in f:
                if line[0] == "Z":
                    self.letterWeights.append(int(line[2:]))
                else:
                    self.letterWeights.append(int(line[2:-1]))

    # @brief        Finds all possible unexplored paths within the board
    # @param[in]    currentPath
    #               a list containing the [x, y] values that have already been visited
    # @param[out]   a list containing [x, y] values that are available to expand
    def findPossiblePaths(self, currentPath):
        mostRecent = currentPath[-1]
        availableMoves=[]

        for x in range(mostRecent[0]-1, mostRecent[0]+1):
            if x < 0 or x >= self.dimen:
                continue
            for y in range(mostRecent[1]-1, mostRecent[0]+1):
                if y < 0 or y >= self.dimen:
                    continue
                if [x, y] not in currentPath:
                    availableMoves . append([x,y])
        return availableMoves

    # @brief    Since my values for a, b, c, and d are educated guesses, this function
    #           finds the best values for each scenario.
    # @details  iterates through every value of a, b, c, and d with every possible number of
    #           expansions to make a dictionary with the best constants for every scenario.
    def findBestConstants(self, printing):
        a = 0
        b = -100
        c = -200
        d = -1000
        expansions = 1
        tempScore = 0

        returnValue = None


        while expansions <= 10000:
            tempScore = 0
            self.constants[expansions] = [0, 0, 0, 0]
            tempWords = set()
            a = 1
            b =1
            c = 1
            d = -1000

            while d <= 1000:
                returnValue = self.scroggle(2, expansions, False, False, a, b, c, d)
                if (returnValue["totalScore"] > tempScore):
                    self.constants[expansions] = [a, b, c, d]
                    tempScore = returnValue["totalScore"]
                    tempWords = returnValue["goodWords"]
                d += 1
            if printing:
                print("Expansion: ", expansions)
                print("a, b, c, d: ", self.constants[expansions])
                print("Score: ", tempScore)
                print("Good words: ", tempWords)
                print()
            expansions += 1



    # @brief    Looks through the frontier and selects the best option to expand
    # @details  This heuristic looks at three pieces of information.
    #           (x) numWordsWithPrefix, (y) averageWordScore, and (z)avgNumLettersAfterPrefix
    #           The 'goodness' equation score = ab + by + cz +d constants I came up with are
    #           a = 2, b = 1, c = -10, d = 30.  If a prefix occurs many times in the
    #           dictionary it will be 'rewarded'.  If the average score of a word
    #           with that prefix is high it is 'rewarded'.  If the average number of letters after
    #           the prefix is low, it is 'rewarded'; having more letters after the prefix decreases
    #           the goodness quickly giving priority to prefixes that show up often and short prefixes.
    # @param[out]   list containing the path that shows the most promise
    # @note     Assumes that each frontier node[3] is a number containing the 'goodness'
    # @note     A significant number of nodes are not appended to the frontier because the heuristic
    #           function is unable to find some prefix to assign a 'goodness' value meaning that we
    #           can eliminate hundreds of nodes for expansion before even comparing it do the dictionary.
    # @note     The popping is done in the scroggle function but for this heuristic the frontier is sorted
    #           with the highest value on the right so nodes are popped from the right.
    def heuristic1(self, word, path, score, a, b, c, d):
        try:
            heuristicScore = (self.numWordsWithPrefix[word] * a) + (self.averageWordScore[word]*b) + (self.avgNumLettersAfterPrefix[word]*c) + d
        except KeyError:
            return
        self.frontier.append([word, path, score, heuristicScore])
        return

    # @brief    Searches the board for goal states
    # @details  Depending on the searchType, it usees BFS, DFS, or A* to
    #           search for goal states which in this case is a word in the dictionary
    #
    # @param[in]    searchType
    #               0 = DFS     1 = BFS     2 = A*(h1)      3 = A*h(2)
    # @param[in[    queryLimit
    #               integer of the number of dictionary queries the solver is allowed
    #               queryLimit < 0 = unlimited      querLimit > 0 = finite
    # @param[in]    dumbness
    #               True for no prefix optimization     False for optimization
    # @params[in]   a, b, c, d
    #               Only used for A* so if A* is selects as the searchType and the values
    #               are not included, -1 is returned
    # @param[out]   -1 if an error, 1 otherwise
    def scroggle(self, searchType, expansionLimit, dumbness, printing, a = -1, b = -1, c = -1, d = -1):
        if (searchType == 2 and a == -1 and b == -1 and c == -1 and d == -1):
            return -1
        if (expansionLimit == 0):
            return -1

        #   Add the individual board tiles to the frontier
        for index, char in enumerate(self.board, start=0):
            try:
                heuristicScore = (self.numWordsWithPrefix[char] * a) + (self.averageWordScore[char] * b) + (self.avgNumLettersAfterPrefix[char] * c) + d
                self.frontier.append([char, [[index % self.dimen, int(index / self.dimen)]], self.getWordScore(char), heuristicScore])
            except KeyError:
                continue

        goodWords =set()

        remainingExpansions = expansionLimit
        dictQueries =0
        expansions = 0

        startTime = time.perf_counter()
        newWord=""
        newPath = []
        newScore = 0
        foundPartial = False
        totalScore = 0

        frontierSize = self.dimen * self.dimen
        maxFrontierSize = self.dimen * self.dimen

        avgDepth = 0
        maxDepth = 0

        avgBranching = 0

        while self.frontier:
            if remainingExpansions==0 and expansionLimit > 0:
                break
            currentPath=[]
            if searchType ==0 or searchType == 2:
                currentPath=self.frontier.pop()
            elif searchType==1:
                currentPath=self.frontier.popleft()
            expansions += 1
            remainingExpansions -= 1

            avgDepth += len(currentPath[0])
            if len(currentPath[0])>maxDepth:
                maxDepth = len(currentPath[0])

            #   Check to see if word is in the dictionary
            foundPartial = False
            if len(currentPath[0]) > 1:
                dictQueries+=1
                try:
                    self.numWordsWithPrefix[currentPath[0]]
                    foundPartial = True
                    if(currentPath[0] in self.dict):
                        goodWords.add(currentPath[0])
                        totalScore += currentPath[2]
                except KeyError:
                    foundPartial = False

            #   Expand nodes and add them to the frontier
            if(foundPartial == True or len(currentPath[0])==1 or dumbness == True):
                availablePaths=self.findPossiblePaths(currentPath[1])
                avgBranching += len(availablePaths)
                if availablePaths == []:
                    continue

                newWord=""
                newPath = list(currentPath[1])
                newScore = 0
                for availablePath in availablePaths:
                    newWord = currentPath[0] + self.board[(self.dimen * availablePath[0]) + availablePath[1]]
                    newPath.append(availablePath)
                    newScore = currentPath[2] + self.letterWeights[ ord(newWord[-1]) - ord('a') ]
                    if searchType == 2:
                        self.heuristic1(newWord, newPath, newScore, a, b, c, d)
                    elif searchType == 0 or searchType == 1:
                        self.frontier.append([newWord, newPath, newScore])
                    newPath=list(currentPath[1])
                frontierSize += len(self.frontier)

                if len(self.frontier) > maxFrontierSize:
                    maxFrontierSize = len(self.frontier)
                #If we are in A* we need to sort the frontier
                if searchType == 2:
                    self.frontier = sorted(self.frontier, key = itemgetter(3))

        returnValues={}
        returnValues["searchType"]=searchType
        returnValues["expansions"]=expansionLimit
        returnValues["totalScore"]=totalScore
        returnValues["goodWords"]=goodWords
        returnValues["avgFrontierSize"]= (frontierSize / (expansions+1))
        returnValues["maxFrontierSize"] = maxFrontierSize
        returnValues["runtime"] = time.perf_counter()-startTime
        returnValues["dictQueries"] = dictQueries
        returnValues["maxFrontierSize"] = maxFrontierSize
        returnValues["avgDepth"] = avgDepth / expansions
        returnValues["maxDepth"] = maxDepth
        returnValues["avgBranching"] = avgBranching / expansions
        if printing:
            self.printEverything(returnValues)
        return returnValues

    def printEverything(self, values):
        if(values["searchType"]==0):
            print("Search Type:  Depth Fisrt Search")
        elif(values["searchType"] == 1):
            print("Search Type: Bredth First Search")
        elif(values["searchType"] == 2):
            print("Searth Type: A* using h1()")

        print("Number of expansions: ", values["expansions"])
        print(len(values["goodWords"]),"Words found:  ", sorted(values["goodWords"]))
        print("Average frontier size:  ", values["avgFrontierSize"])
        print("Max frontier size:  ", values["maxFrontierSize"])
        print("Average depth:  ", values["avgDepth"])
        print("Average brancing factor:  ", values["avgBranching"])
        print("Total score:  ", values["totalScore"])



scroggleInstance = Scroggle()
scroggleInstance.importWeights("scrabble-vals.txt")
scroggleInstance.importBoard("fourboard2.txt")
scroggleInstance.importDictionary("dict.txt")
score = scroggleInstance.scroggle(3,300,True)
#scroggleInstance.scroggle(3,-1,True, 2,1,-10,30)
