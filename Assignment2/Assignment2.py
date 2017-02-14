import time
from collections import deque

class Scroggle(object):

    def __init__(self):
        self.dimen=0
        self.frontier=[]
        self.board=[]
        self.numQueries=0
        self.dict=set()
        self.numWordsWithPrefix = {}
        self.averageWordScore = {}
        self.avgNumLettersAfterPrefix = {}
        self.letterWeights = []
        self.goodWords = set()


    def importBoard(self, boardFile):
        with open(boardFile) as f:
            for xindex, line in enumerate(f, start=0):
                letters=line.split()
                for yindex, char in enumerate(letters, start=0):
                    self.board.append(char.lower())
                    self.frontier.append([char.lower(), [[xindex, yindex]], self.letterWeights[ord(char.lower())-ord('a')]])
            self.dimen=xindex+1
        self.frontier=deque(self.frontier)

    #I handle the qu case by adding the word with adn without the u in the word.
    #As per the instructions, a board with the word 'qeen' should be translated as 'queen'.
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


    def getWordScore(self, word):
        wordScore = 0
        for char in word:
            wordScore += self.letterWeights[ord(char) - ord('a')]
        return wordScore

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

    def heuristic1(self):
        return


    # @brief    Searches the board for goal states
    # @details  Depending on the searchType, it usees BFS, DFS, or A* to
    #           search for goal states which in this case is a word in the dictionary
    #
    # @param[in]    searchType
    #               0 = DFS     1 = BFS     2 = A*
    # @param[in[    queryLimit
    #               integer of the number of dictionary queries the solver is allowed
    #               queryLimit < 0 = unlimited      querLimit > 0 = finite
    # $param[in]    dumbness
    #               True for no prefix optimization     False for optimization
    def scroggle(self, searchType, queryLimit, dumbness):
        if(queryLimit == 0):
            return -1
        self.numQueries = queryLimit

        dictQueries =0
        startTime = time.perf_counter()
        newWord=""
        newPath = []
        newScore = 0
        foundPartial = False

        while self.frontier:
            if self.numQueries==0 and queryLimit > 0:
                return

            currentPath=[]
            if searchType ==0:
                currentPath=self.frontier.pop()
            elif searchType==1:
              currentPath=self.frontier.popleft()






            #   Check to see if word is in the dictionary
            foundPartial = False
            if len(currentPath[0]) > 1:
                self.numQueries-=1
                dictQueries+=1
                try:
                    self.numWordsWithPrefix[currentPath[0]]
                    foundPartial = True
                    if(currentPath[0] in self.dict):
                        self.goodWords.add(currentPath[0])
                except KeyError:
                    foundPartial = False

            #   Expand nodes and add them to the frontier
            if(foundPartial == True or len(currentPath[0])==1 or dumbness == True):
                availablePaths=self.findPossiblePaths(currentPath[1])
                if availablePaths == []:
                    continue

                newWord=""
                newPath = list(currentPath[1])
                newScore = 0
                for availablePath in availablePaths:
                    newWord = currentPath[0] + self.board[(self.dimen * availablePath[0]) + availablePath[1]]
                    newPath.append(availablePath)
                    newScore = currentPath[2] + self.letterWeights[ ord(newWord[-1]) - ord('a') ]
                    self.frontier.append([newWord, newPath, newScore ])
                    newPath=list(currentPath[1])
        print("Solver runtime: ", time.perf_counter()-startTime)
        print("Dict queries: ", dictQueries)



scroggleInstance = Scroggle()
scroggleInstance.importWeights("scrabble-vals.txt")
scroggleInstance.importBoard("fourboard2.txt")
scroggleInstance.importDictionary("dict.txt")
scroggleInstance.scroggle(0,-1,False)
print(scroggleInstance.numWordsWithPrefix["az"])
