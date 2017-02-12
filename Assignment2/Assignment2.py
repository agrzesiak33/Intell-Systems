import math
from collections import deque

class Scroggle(object):

    def __init__(self):
        self.dimen=0
        self.frontier=[]
        self.board=[]
        self.numQueries=0
        self.dictPrefix = set()
        self.dict=set()
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
        tempString = ""
        for letter in word:
            if tempString=="":
                tempString+=letter
            elif tempString[-1]=="q" and letter=="u":
                continue
            else:
                tempString+=letter

        for i in range(len(tempString) - 1):
            if i == (len(tempString) - 2):
                self.dict.add(tempString)
                self.dictPrefix.add(tempString)
            else:
                self.dictPrefix.add(tempString[:i + 2])

    def importDictionary(self, dictFile):
        lastLine=""
        with open(dictFile) as f:
            for word in f:
                word = word[:-1]
                lastline=word
                if "qu" in word:
                    self.handleQU(word)
                for i in range(len(word)-1):
                    if i==(len(word)-2):
                        self.dict.add(word)
                        self.dictPrefix.add(word)
                    else:
                        self.dictPrefix.add(word[:i + 2])
        self.dict.add(lastline)
        self.dictPrefix.add(lastline)

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

        for x in range(currentPath[0]-1, currentPath[0]+1):
            if x < 0 or x >= self.dimen:
                continue
            for y in range(currentPath[1]-1, currentPath[0]+1):
                if y < 0 or y >= self.dimen:
                    continue
                if [x, y] not in currentPath:
                    availableMoves . append([x,y])
        return availableMoves


    # @brief    Searches the board for goal states
    # @details  Depending on the searchType, it usees BFS, DFS, or A* to
    #           search for goal states which in this case is a word in the dictionary
    #
    # @param[in]    searchType
    #               0 = DFS     1 = BFS     2 = A*
    def scroggle(self, searchType):
        if self.numQueries==0:
            return

        currentPath=[]
        if searchType ==0:
            currentPath=self.frontier.pop()
        elif searchType==1:
          currentPath=self.frontier.popLeft()

        foundPartial = False
        if len(currentPath[0]) > 1:
            self.numQueries-=1
            if (currentPath[0] in self.dictPrefix):
                foundPartial = True
                if currentPath[0] in self.dict:
                    self.goodWords.add(currentPath[0])

        if(foundPartial == True):
            availablePaths=self.findPossiblePaths(currentPath[1])




scroggleInstance = Scroggle()
scroggleInstance.importWeights("scrabble-vals.txt")
scroggleInstance.importBoard("twoboard.txt")
scroggleInstance.importDictionary("dict.txt")
print(scroggleInstance.frontier)
