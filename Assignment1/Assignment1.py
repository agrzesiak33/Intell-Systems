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
        self.dictPrefix = [set() for i in range(20)]
        self.dict=[set() for i in range(20)]
        with open(dictFile) as f:
            for word in f:
                word = word[:-1]
                # every prefix of every length
                for i in range(len(word)-1):
                    if i==(len(word)-2):
                        #temp = word + "_"
                        #self.dictPrefix[i].add(temp)
                        self.dict[i].add(word)
                    else:
                        self.dictPrefix[i].add(word[:i + 2])

    def boggle(self):
        self.numberOfMoves=0
        self.numberQueries=0
        startTime= time.time()
        self.goodWords = []
        self.dimen = int(math.sqrt(len(self.board)))
        for index, letter in enumerate(self.board, start=0):
            currentWordIndicies=[index]
            currentWordLetters=letter
            tempTime=time.time()
            self.recBoggle(currentWordLetters, currentWordIndicies)
            print(index, " ", letter, " ", time.time()-tempTime)
            print("Number of moves: ", self.numberOfMoves)
            print("Number of queries: ", self.numberQueries)
            print()
        endTime = time.time()-startTime
        self.goodWords = list(set(self.goodWords))
        self.goodWords.sort()
        print ("Good words", self.goodWords)
        print ("Length of good words", len(self.goodWords))
        print ("Time: ", endTime)
        print ("Number of moves: ",self.numberOfMoves)
        print ("Number of full dict queries: ", self.numberQueries)

    def recBoggle(self, currentWordLetters, currentWordIndicies):
        foundPartial = False
        if len(currentWordLetters)>1:
            self.numberOfMoves += 1
            if(currentWordLetters in self.dictPrefix[len(currentWordLetters)-2]):
                foundPartial=True
                if currentWordLetters in self.dict[len(currentWordLetters)-2]:
                    self.goodWords.append(currentWordLetters)
                    self.numberQueries+=1


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
                if (currentWordIndicies[-1] > self.dimen - 1) and (currentWordIndicies[-1]-self.dimen-1) not in currentWordIndicies:
                    temp.append(currentWordIndicies[-1] - self.dimen - 1)
                    self.recBoggle(currentWordLetters + self.board[temp[-1]],
                                   temp)
                    temp=list(currentWordIndicies)
                #room to move left and down
                if (currentWordIndicies[-1] < (len(self.board) - self.dimen)) and (currentWordIndicies[-1] + self.dimen -1) not in currentWordIndicies:
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
                if currentWordIndicies[-1] > self.dimen - 1 and currentWordIndicies[-1]-self.dimen +1 not in currentWordIndicies:
                    temp.append(currentWordIndicies[-1] - self.dimen + 1)
                    self.recBoggle(currentWordLetters + self.board[temp[-1]],
                                   temp)
                    temp=list(currentWordIndicies)
                # room to move right and down
                if currentWordIndicies[-1] < (len(self.board) - self.dimen - 1) and currentWordIndicies[-1]+self.dimen+1 not in currentWordIndicies:
                    temp.append(currentWordIndicies[-1] + self.dimen + 1)
                    self.recBoggle(currentWordLetters + self.board[temp[-1]],
                                   temp)
                    temp=list(currentWordIndicies)
            #below row 0, room to move up
            if currentWordIndicies[-1] > self.dimen-1 and currentWordIndicies[-1] - self.dimen not in currentWordIndicies:
                temp.append(currentWordIndicies[-1] - self.dimen)
                self.recBoggle(currentWordLetters + self.board[temp[-1]],
                               temp)
                temp=list(currentWordIndicies)
            #above row -1, room to move down
            if currentWordIndicies[-1]<(len(self.board)-self.dimen) and currentWordIndicies[-1] +self.dimen not in currentWordIndicies:
                temp.append(currentWordIndicies[-1] + self.dimen)
                self.recBoggle(currentWordLetters + self.board[temp[-1]],
                               temp)
                temp=list(currentWordIndicies)


boggleInstance = Boggle()
boggleInstance.importBoard("board.txt")
boggleInstance.importDictionary("dict.txt")
# for i in range(4):
#     print (boggleInstance.dictPrefix[i])
#     print (len(boggleInstance.dictPrefix[i]))
#print (boggleInstance.board)
#print (boggleInstance.dict)

boggleInstance.boggle()