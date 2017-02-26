import time
from collections import deque
from operator import itemgetter
import random

class Scroggle(object):

    def __init__(self):
        self.dimen=0
        self.frontier=deque()
        self.board=[]
        self.numQueries=0
        self.dict=set()
        self.numWordsWithPrefix = {}
        self.averageWordScoreAfterPrefix = {}
        self.avgNumLettersAfterPrefix = {}
        self.letterWeights = []
        self.constants = {}
        #These values are the result of running an exhaustive search for the constants across 50 boards.

        self.calculatedConstants4x4 = {0: [0.0, 0.0, 0.0], 1: [-4.99, -300.0, -290.0], 2: [-6.22, -172.5, -110.0],
                                       3: [-7.44, -330.0, -447.5], 4: [-6.68, -372.5, -255.0],
                                       5: [-6.29, -577.5, -320.0],6: [-5.89, -535.0, -437.5],
                                       7: [-4.31, -252.5, -337.5], 8: [-4.31, -450.0, -272.5],
                                       9: [-3.89, -412.5, -235.0], 10: [-4.44, -440.0, -450.0],
                                       11: [-4.17, -430.0, -252.5],12: [-3.44, -382.5, -472.5],
                                       13: [-2.89, -282.5, -490.0], 14: [-2.65, -412.5, -380.0],
                                       15: [-3.03, -387.5, -347.5], 16: [-3.07, -467.5, -437.5],
                                       17: [-3.27, -270.0, -625.0],18: [-2.68, -482.5, -465.0],
                                       19: [-3.11, -415.0, -535.0], 20: [-2.6, -387.5, -617.5],
                                       21: [-2.47, -535.0, -627.5], 22: [-2.11, -582.5, -662.5],
                                       23: [-2.13, -595.0, -722.5],24: [-2.12, -607.5, -610.0],
                                       25: [-2.08, -577.5, -767.5], 26: [-2.63, -477.5, -687.5],
                                       27: [-2.64, -615.0, -597.5], 28: [-2.7, -625.0, -695.0],
                                       29: [-3.16, -492.5, -755.0],30: [-2.59, -532.5, -885.0],
                                       31: [-2.71, -642.5, -812.5], 32: [-2.97, -562.5, -775.0],
                                       33: [-3.21, -697.5, -807.5], 34: [-2.64, -602.5, -640.0],
                                       35: [-2.25, -492.5, -760.0],36: [-2.59, -525.0, -837.5],
                                       37: [-2.43, -465.0, -812.5], 38: [-2.58, -592.5, -822.5],
                                       39: [-2.93, -587.5, -962.5], 40: [-3.23, -645.0, -867.5],
                                       41: [-3.57, -745.0, -892.5],42: [-3.27, -777.5, -902.5],
                                       43: [-4.07, -805.0, -847.5], 44: [-4.03, -772.5, -867.5],
                                       45: [-3.54, -860.0, -847.5], 46: [-3.54, -795.0, -850.0],
                                       47: [-4.0, -812.5, -860.0],48: [-3.98, -840.0, -892.5],
                                       49: [-3.92, -885.0, -875.0], 50: [-3.85, -785.0, -812.5],
                                       51: [-4.55, -822.5, -835.0], 52: [-4.56, -835.0, -942.5],
                                       53: [-4.89, -817.5, -940.0],54: [-4.68, -762.5, -960.0],
                                       55: [-4.78, -885.0, -1057.5], 56: [-4.77, -895.0, -1020.0],
                                       57: [-5.15, -907.5, -1102.5], 58: [-4.99, -877.5, -1055.0],
                                       59: [-5.08, -945.0, -990.0]}

        self.calculatedConstants3x3 = {0: [0.0, 0.0, 0.0], 1: [-6.06, -365.0, -265.0], 2: [-7.91, -380.0, -187.5],
                                       3: [-7.74, -455.0, -300.0], 4: [-5.63, -197.5, -235.0],
                                       5: [-5.16, -330.0, -117.5],6: [-4.35, -367.5, -152.5],
                                       7: [-3.51, -275.0, -52.5], 8: [-3.41, -255.0, -562.5],
                                       9: [-3.66, -270.0, -240.0], 10: [-2.9, -402.5, -87.5],
                                       11: [-2.98, -195.0, -137.5],12: [-3.45, -247.5, -230.0],
                                       13: [-4.11, -315.0, -155.0], 14: [-2.96, -477.5, -105.0],
                                       15: [-3.67, -452.5, -260.0], 16: [-3.94, -412.5, -377.5],
                                       17: [-4.07, -495.0, -165.0],18: [-3.13, -502.5, -227.5],
                                       19: [-3.02, -417.5, -172.5], 20: [-2.98, -407.5, -122.5],
                                       21: [-2.8, -365.0, -355.0], 22: [-2.72, -300.0, -490.0],
                                       23: [-3.06, -335.0, -200.0],24: [-2.4, -345.0, -285.0],
                                       25: [-2.59, -380.0, -450.0], 26: [-2.52, -610.0, -382.5],
                                       27: [-2.3, -595.0, -395.0], 28: [-2.26, -550.0, -465.0],
                                       29: [-1.84, -595.0, -492.5],30: [-2.3, -635.0, -402.5],
                                       31: [-1.79, -612.5, -607.5], 32: [-2.32, -552.5, -700.0],
                                       33: [-2.19, -560.0, -687.5], 34: [-2.18, -642.5, -602.5],
                                       35: [-1.5, -582.5, -602.5],36: [-1.83, -635.0, -530.0],
                                       37: [-2.33, -635.0, -555.0], 38: [-2.44, -752.5, -625.0],
                                       39: [-2.22, -630.0, -657.5], 40: [-2.22, -652.5, -615.0],
                                       41: [-2.05, -647.5, -635.0],42: [-2.65, -610.0, -757.5],
                                       43: [-3.05, -772.5, -655.0], 44: [-2.99, -785.0, -710.0],
                                       45: [-3.6, -802.5, -680.0], 46: [-3.88, -772.5, -750.0],
                                       47: [-4.52, -805.0, -607.5],48: [-3.93, -827.5, -600.0],
                                       49: [-3.42, -720.0, -737.5], 50: [-3.28, -732.5, -745.0],
                                       51: [-3.74, -790.0, -772.5], 52: [-3.67, -835.0, -762.5],
                                       53: [-2.95, -742.5, -715.0],54: [-3.5, -757.5, -662.5],
                                       55: [-3.63, -735.0, -777.5], 56: [-3.74, -715.0, -792.5],
                                       57: [-3.68, -700.0, -845.0], 58: [-3.58, -775.0, -880.0],
                                       59: [-4.06, -745.0, -932.5]}


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
    def importDictionary(self, dictFile, printing = False):
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
                    #If the whole word is there
                    if i==(len(word)-1):
                        self.dict.add(word)
                        try:
                            self.numWordsWithPrefix[word] += 1
                        except KeyError:
                            self.numWordsWithPrefix[word] = 1
                            self.avgNumLettersAfterPrefix[word] = 0
                            self.averageWordScoreAfterPrefix[word] = 0
                    else:
                        prefix = word[:i + 1]
                        #   If the prefix has already been encounteres
                        try:
                            oldAverage = self.averageWordScoreAfterPrefix[prefix] * self.numWordsWithPrefix[prefix]
                            newAverage = (oldAverage + self.getWordScore(lastline[i+1:]))
                            newAverage /= (self.numWordsWithPrefix[prefix] + 1)
                            self.averageWordScoreAfterPrefix[prefix] = newAverage

                            oldAverage = self.avgNumLettersAfterPrefix[prefix] * self.numWordsWithPrefix[prefix]
                            newAverage = (oldAverage + len(word)-i-1)
                            newAverage /= (self.numWordsWithPrefix[prefix] +1)
                            self.avgNumLettersAfterPrefix[prefix] = newAverage

                            self.numWordsWithPrefix[prefix] += 1

                        #   If the prefix is new
                        except KeyError:
                            self.numWordsWithPrefix[prefix] = 1
                            self.averageWordScoreAfterPrefix[prefix] = self.getWordScore(lastline[i+1:])
                            self.avgNumLettersAfterPrefix[prefix] = len(word)-i-1
        self.dict.add(lastline)
        self.addTo_numWordsWithPrefix(lastline)
        if printing:
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

    # @brief    once a board has already been initlized, this overwrites the current board with a new one.
    def getRandomBoard(self):
        for i in range(self.dimen * self.dimen):
            self.board[i] = chr(random.randint(0, 25) + ord('a'))

    def loadBoard(self, chars):
        for index, char in enumerate(chars, start=0):
            self.board[index] = char

    # @brief        Finds all possible unexplored paths within the board
    # @param[in]    currentPath
    #               a list containing the [x, y] values that have already been visited
    # @param[out]   a list containing [x, y] values that are available to expand
    def findPossiblePaths(self, currentPath):
        mostRecent = currentPath[-1]
        availableMoves=[]

        for x in range(mostRecent[0]-1, mostRecent[0]+2):
            if x < 0 or x >= self.dimen:
                continue

            for y in range(mostRecent[1]-1, mostRecent[1]+2):
                if y < 0 or y >= self.dimen:
                    continue
                if [x, y] not in currentPath:
                    availableMoves . append([x,y])
        return availableMoves

    # @brief    This function will generate random boards and calculate the best a, b, and c
    #           values for every expansion up until
    # @details  iterates through every value of a, b, c with every possible number of
    #           expansions to make a dictionary with the best constants for every scenario.
    # @param[in]    printing
    #               A boolean value to determine whether or not to print everything
    def findBestConstants(self, printing):
        print("Finding best constants...")
        a = -5
        b = -100
        c = -200
        expansions = 1
        tempScore = 0
        averageA = 0
        averageB = 0
        averageC = 0
        constantsExtensionsBoards = [[[0, 0, 0] for i in range(40)] for j in range(50)]

        for board in range(50):
            print("On board ",board)
            averageA = 0
            averageB = 0
            averageC = 0
            tempScore = 0


            self.getRandomBoard()
            expansions=1

            while expansions <= 60:
                a=-20
                b=-2000
                c=-2000
                tempScore = 0
                tempWords = set()

                while a <= 20:
                    b= -2000
                    while b <= 2000:
                        c= -2000
                        while c <= 2000:
                            returnValue = self.scroggle(2, expansions, False, False, a, b, c, True)
                            if (returnValue["totalScore"] > tempScore):
                                temp = expansions-1
                                constantsExtensionsBoards[board][temp] = [a,b,c]
                                tempScore = returnValue["totalScore"]
                                tempWords = returnValue["goodWords"]
                            c+=250
                        b += 250
                    a += 1
                expansions+=1
        for expansion in range(len(constantsExtensionsBoards[0])):
            averageA = 0
            averageB = 0
            averageC = 0
            for boardConstants in constantsExtensionsBoards:
                averageA += boardConstants[expansion][0]
                averageB += boardConstants[expansion][1]
                averageC += boardConstants[expansion][2]
            averageA /= len(constantsExtensionsBoards)
            averageB /= len(constantsExtensionsBoards)
            averageC /= len(constantsExtensionsBoards)
            self.constants[expansion]=[averageA, averageB, averageC]





    # @brief    Looks through the frontier and selects the best option to expand
    # @details  This heuristic looks at three pieces of information.
    #           (x) numWordsWithPrefix, (y) averageWordScore, and (z)avgNumLettersAfterPrefix
    #           The 'goodness' equation score = ab + by + cz constants I found for an average 4x4 board are
    #           a = -3, b = -6750, c = -2250.
    # @param[out]   list containing the path that shows the most promise
    # @note     Assumes that each frontier node[3] is a number containing the 'goodness'
    # @note     A significant number of nodes are not appended to the frontier because the heuristic
    #           function is unable to find some prefix to assign a 'goodness' value meaning that we
    #           can eliminate hundreds of nodes for expansion before even comparing it do the dictionary.
    # @note     The popping is done in the scroggle function but for this heuristic the frontier is sorted
    #           with the highest value on the right so nodes are popped from the right.
    def heuristic1(self, word, path, score, a, b, c):
        try:
            heuristicScore = (self.numWordsWithPrefix[word] * a) + (self.averageWordScore[word]*b) + (self.avgNumLettersAfterPrefix[word]*c)
        except KeyError:
            heuristicScore = -99999999999
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
    # @params[in]   a, b, c,
    #               Only used for A* so if A* is selects as the searchType and the values
    #               are not included, -1 is returned
    # @param[out]   -1 if an error, 1 otherwise
    def scroggle(self, searchType, expansionLimit, dumbness, printing, a = -1, b = -1, c = -1, testing = False):
        self.frontier = deque()
        if testing == False:
            try:
                constants = self.constants[expansionLimit]
            except:
                constants = self.constants[49]
            a = constants[0]
            b = constants[1]
            b = constants[2]

        if (searchType == 2 and a == -1 and b == -1 and c == -1):
            return -1
        if (expansionLimit == 0):
            return -1

        #   Add the individual board tiles to the frontier
        for index, char in enumerate(self.board, start=0):
            try:
                heuristicScore = (self.numWordsWithPrefix[char] * a) + (self.averageWordScore[char] * b) + (self.avgNumLettersAfterPrefix[char] * c)
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
                        self.heuristic1(newWord, newPath, newScore, a, b, c)
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
#score = scroggleInstance.scroggle(1,300, True, True)
#scroggleInstance.scroggle(2,30,False, True)

#exit()


####FROM HERE DOWN IS JUST OPTIMIZATION STUFF TO PLAY WITH CONSTANTS#########
scroggleInstance.getRandomBoard()
scroggleInstance.findBestConstants(True)
print(scroggleInstance.constants)
exit()

scores = [0,0,0,0]
for i in range(2000):
    scroggleInstance.getRandomBoard()
    tempValues = [0,0,0,0]

    values = scroggleInstance.scroggle(2, 10, False, False, -5, -5000, -2250)
    tempValues[0] = values["totalScore"]

    values = scroggleInstance.scroggle(2, 10, False, False, -5, -6750, -2250)
    tempValues[1] = values["totalScore"]

    values = scroggleInstance.scroggle(2, 10, False, False, -6, -5000, -2250)
    tempValues[2] = values["totalScore"]

    values = scroggleInstance.scroggle(2, 10, False, False, -3, -6750, -2250)
    tempValues[3] = values["totalScore"]

    for i in range(4):
        if tempValues[i] == max(tempValues):
            scores[i]+=1
minScore = min(scores)
for i in range(4):
    scores[i] -= minScore
print(scores)
exit()
scroggleInstance.scroggle(2,30,False, True, -10,-100,100)
print()
scroggleInstance.scroggle(2,30,False, True, -1000,-100,100)
print()
scroggleInstance.scroggle(2,30,False, True, -3000,-100,100)
print()
scroggleInstance.scroggle(2,30,False, True, -1000,-5000,100)
print()
#scroggleInstance.findBestConstants(True)