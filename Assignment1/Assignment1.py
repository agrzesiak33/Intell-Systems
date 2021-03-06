import math
import time

class Boggle(object):

    def importBoard(self, boardFile):
        self.board=[]
        with open(boardFile) as f:
            for line in f:
                letters=line.split()
                for char in letters:
                    self.board.append(char.lower())

    def importDictionary(self, dictFile):
        #dictPrefix is a list of sets
        #list[0] contains a list with prefixes of length 2
        #list[1] contains a list with prefixes of length 3 adn so on
        self.dictPrefix = [set() for i in range(20)]
        #dict is a set containg the actual dictionary with all full words
        self.dict=[set() for i in range(20)]
        lastLine=""
        with open(dictFile) as f:
            for word in f:
                word = word[:-1]
                lastline=word
                #Handeling the q case
                if "qu" in word:
                    self.handleQU(word)
                    #iterates through the word and adds every version of the word starting with
                    #the first letter
                for i in range(len(word)-1):
                    if i==(len(word)-2):
                        self.dict[i].add(word)
                        self.dictPrefix[i].add(word)
                    else:
                        self.dictPrefix[i].add(word[:i + 2])
        self.dict[len(lastline)-2].add(lastline)
        self.dictPrefix[len(lastline)-2].add(lastline)

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
                self.dict[i].add(tempString)
                self.dictPrefix[i].add(tempString)
            else:
                self.dictPrefix[i].add(tempString[:i + 2])

    def printEverything(self, timeTaken):
        print("CURRENT BOARD: ", self.dimen, "X", self.dimen)
        print()
        print("Searched total of ", self.numberOfMoves, "moves in ", timeTaken, "seconds")
        print()
        allWords=list()
        for index, solution in enumerate(self.goodWords, start=2):
            if solution:
                allWords.extend(list(solution))
                print(index, '\t', "-letter words: ", list(solution))
        print()
        print("Found ", len(allWords), " words in total. \nAlphabetically sorted list:")
        allWords.sort()
        print(allWords)

    def boggle(self):
        self.numberOfMoves=0
        startTime= time.perf_counter()
        self.goodWords = [set() for i in range(20)]
        self.dimen = int(math.sqrt(len(self.board)))
        for index, letter in enumerate(self.board, start=0):
            currentWordIndicies=[index]
            currentWordLetters=letter
            tempTime=time.time()
            self.recBoggle(currentWordLetters, currentWordIndicies)
        endTime = time.perf_counter()-startTime
        self.printEverything(endTime)
        return endTime

    def recBoggle(self, currentWordLetters, currentWordIndicies):
        foundPartial = False
        if len(currentWordLetters)>1:
            self.numberOfMoves += 1
            #If the sequence of letters is in the prefix dictionary, we acknowledge that we found
            #a partial word and need to do more searching, then we check to see if the sequence
            # is actually a word and if it is, it gets added to the found set.
            if(currentWordLetters in self.dictPrefix[len(currentWordLetters)-2]):
                foundPartial=True
                if currentWordLetters in self.dict[len(currentWordLetters)-2]:
                    self.goodWords[len(currentWordLetters)-2].add(currentWordLetters)

        #everything in here is checking the positions around the current letter and recursively calling
        # itself if it is an open position.
        if foundPartial == True or len(currentWordLetters) == 1:
            temp=list(currentWordIndicies)
            #right of col 0, room to move left
            if currentWordIndicies[-1]%self.dimen!=0:
                if(currentWordIndicies[-1] - 1) not in currentWordIndicies:
                    temp.append(currentWordIndicies[-1] - 1)
                    self.recBoggle(currentWordLetters + self.board[temp[-1]],
                                   temp)
                    temp=list(currentWordIndicies)
                #room to move left and up
                if (currentWordIndicies[-1] > self.dimen - 1) and \
                                (currentWordIndicies[-1]-self.dimen-1) not in currentWordIndicies:
                    temp.append(currentWordIndicies[-1] - self.dimen - 1)
                    self.recBoggle(currentWordLetters + self.board[temp[-1]],
                                   temp)
                    temp=list(currentWordIndicies)
                #room to move left and down
                if (currentWordIndicies[-1] < (len(self.board) - self.dimen)) and \
                                (currentWordIndicies[-1] + self.dimen -1) not in currentWordIndicies:
                    temp.append(currentWordIndicies[-1] + self.dimen-1)
                    self.recBoggle(currentWordLetters + self.board[temp[-1]],
                                   temp)
                    temp=list(currentWordIndicies)
            #left of col -1, room to move right
            if (currentWordIndicies[-1]+1)%self.dimen!=0:
                if currentWordIndicies[-1] + 1 not in currentWordIndicies:
                    temp.append(currentWordIndicies[-1]+1)
                    self.recBoggle(currentWordLetters + self.board[temp[-1]],
                                   temp)
                    temp=list(currentWordIndicies)
                # room to move right and up
                if currentWordIndicies[-1] > self.dimen - 1 and \
                                                currentWordIndicies[-1]-self.dimen +1 not in currentWordIndicies:
                    temp.append(currentWordIndicies[-1] - self.dimen + 1)
                    self.recBoggle(currentWordLetters + self.board[temp[-1]],
                                   temp)
                    temp=list(currentWordIndicies)
                # room to move right and down
                if currentWordIndicies[-1] < (len(self.board) - self.dimen - 1) and \
                                                currentWordIndicies[-1]+self.dimen+1 not in currentWordIndicies:
                    temp.append(currentWordIndicies[-1] + self.dimen + 1)
                    self.recBoggle(currentWordLetters + self.board[temp[-1]],
                                   temp)
                    temp=list(currentWordIndicies)
            #below row 0, room to move up
            if currentWordIndicies[-1] > self.dimen-1 and \
                                    currentWordIndicies[-1] - self.dimen not in currentWordIndicies:
                temp.append(currentWordIndicies[-1] - self.dimen)
                self.recBoggle(currentWordLetters + self.board[temp[-1]],
                               temp)
                temp=list(currentWordIndicies)
            #above row -1, room to move down
            if currentWordIndicies[-1]<(len(self.board)-self.dimen) and \
                                    currentWordIndicies[-1] +self.dimen not in currentWordIndicies:
                temp.append(currentWordIndicies[-1] + self.dimen)
                self.recBoggle(currentWordLetters + self.board[temp[-1]],
                               temp)
                temp=list(currentWordIndicies)


boggleInstance = Boggle()
boggleInstance.importBoard("tenboard2.txt")
boggleInstance.importDictionary("dict.txt")
# for i in range(4):
#     print (boggleInstance.dictPrefix[i])
#     print (len(boggleInstance.dictPrefix[i]))
#print (boggleInstance.board)
#print (boggleInstance.dict)
boggleInstance.boggle()