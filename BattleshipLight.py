print("Hunt begins.\n")

# GLOBALS

WTR="~"
HIT="H"
MSS="*"
SNK="S"

DEFAULT_WGT = 0
PSBLPOS_WGT = 1
LATTICE_WGT = 2 # Weight of lattice pattern
KILLBOX_WGT = 100 # Weight of killbox pattern

GameOver = False

Ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
# class Ship:
#     def __init__(self, len):
#         self.length = len
#         self.isSunk = False
# ShipList = []
# for s in SHIP_LENGTHS:
#     ShipList.append(Ship(s))



# OBJECTS

class Spot:
    def __init__(self):
        self.state = WTR
        self.value = DEFAULT_WGT
    # def __init__(self, xCord:int, yCord:int):
    #     self.state = WTR
    #     self.val = 0
    #     self.x = xCord
    #     self.y = yCord
    def setState(self, st):
        if st=="M":
            self.state=MSS 
        elif st=="H":
            self.state=HIT
        elif st=="S":
            self.state=SNK
        elif st=="W":
            self.state=WTR
    def prntValue(self):
        if self.value<=9:
            print(" ",int(self.value),"  ",sep="",end="")
        elif self.value<=99:
            print(" ",int(self.value)," ",sep="",end="")
        else:
            print(int(self.value)," ",sep="",end="")
    def prntState(self):
        print(" ",self.state,"  ",sep="",end="")
     
Board=[]
for col in range (0, 10):
    c = []
    for row in range (0, 10):
        c.append(Spot())
    Board.append(c)



# UTIL FUNCTIONS

def inBounds(y, x): # DEBUG?
    return y>=0 and y<=9 and x>=0 and x<=9

# def buildLattice(seekSize: int):
#     for x, col in enumerate(Board):
#         for y, spt in enumerate(col):
#             if spt.state==WTR and (x+y)%seekSize==0: # if (RowIndex+ColIndex)%shipLength==0 : then part of target matrix (0-based) sum of the row and column indices and check if they’re divisible by five. If they are, the square is in our shot pattern. We can generalize this idea to any ship length.
#                 spt.val = spt.val + LATTICE_WGT
#                 TargetList.append(spt)

# getNeighbors(x, y): # Returns list of neighbors

def possibleSpot(y:int, x:int):
    return inBounds(y, x) and Board[y][x].state==WTR

def resetValues():
    for y, line in enumerate(Board):
        for x, spt in enumerate(line):
            spt.value = DEFAULT_WGT



# CORE FUNCTIONS

def calibrate():
    resetValues()
    for length in Ships:
        for row in range(0, 10):
            for col in range(0, 10):
                x_validPlace = True
                y_validPlace = True
                for i in range(0, length):
                    if not possibleSpot(row,col+i):
                        x_validPlace=False
                    if not possibleSpot(row+i,col):
                        y_validPlace=False
                if x_validPlace:
                    for i in range(0, length):
                        Board[row][col+i].value += PSBLPOS_WGT
                if y_validPlace:
                    for i in range(0, length):
                        Board[row+i][col].value += PSBLPOS_WGT

    # int maxShipSz = head->getShipSz();

	# 	//Setting horizontal placements
	# 	for (int y = 0; y < BoardSize; y++) {//Iterates rows
	# 		for (int x = 0; x <= BoardSize - maxShipSz; x++) {//Iterates colums
	# 			int xRun = 0;

	# 			for (int i = x; i < x + maxShipSz; i++)
	# 				if (!validTarget(Grid[y][i].getStatus()))
	# 					i = BoardSize;//Breaking out
	# 				else
	# 					xRun++;

	# 			for (ShipLNode* curShip = head; curShip != nullptr; curShip = curShip->next()) 
	# 				if (curShip->getShipSz() <= xRun) 
	# 					for (int i = x; i < x + curShip->getShipSz(); i++) 
	# 						PMap[y][i]++;
	# 		}//End of column iteration
	# 	}//End of row iteration




    # for y, line in enumerate(Board):
        
    #     for x, spt in enumerate(line):
    #         spt.value = 1 # WORKHERE

    # WORKHERE



def printBoard(printValues:bool):
    print("\n##    1   2   3   4   5   6   7   8   9   10\n")
    for y, line in enumerate(Board):
        if y<9: # For line number
            print(" ",end="") # For line number
        print(y+1," [ ",sep="",end="") # For line number
        for x, spt in enumerate(line):
            spt.prntValue() if printValues else spt.prntState()
        print("]\n") # End of line



def recordShot():
    x = int(input("\nX cord of shot: ")) - 1
    y = int(input("Y cord of shot: ")) - 1
    res = input("Result (H, M, or S): ")
    if res=="M":
        Board[y][x].state = MSS
    elif res=="H":
        Board[y][x].state = HIT
    elif res=="S":
        axis = input("X-axis or Y-axis? ")
        coord = int(input("Cordinate: ")) - 1
        if axis=="X" or axis=="Y":
            axisIsX = True if axis=="X" else False
            start = min((x if axisIsX else y), coord)
            end = max((x if axisIsX else y), coord)

            for i in range(start-1, end+2):
                if axisIsX:
                    Board[y][i].state = SNK
                    Board[y][i].value = 0
                    if inBounds(y-1,i):
                        Board[y-1][i].state = MSS
                        Board[y-1][i].value = 0
                    if inBounds(y+1,i):
                        Board[y+1][i].state = MSS
                        Board[y+1][i].value = 0
                    
                else:
                    Board[i][x].state = SNK
                    Board[i][x].value = 0
                    if inBounds(i,x-1):
                        Board[i][x-1].state = MSS
                        Board[i][x-1].value = 0
                    if inBounds(i,x+1):
                        Board[i][x+1].state = MSS
                        Board[i][x+1].value = 0
            if axisIsX:
                if inBounds(y,start-1):
                    Board[y][start-1].state = MSS
                    Board[y][start-1].value = 0
                if inBounds(y,end+1):
                    Board[y][end+1].state = MSS
                    Board[y][end+1].value = 0
            else:
                if inBounds(start-1,x):
                    Board[start-1][x].state = MSS
                    Board[start-1][x].value = 0
                if inBounds(end+1,x):
                    Board[end+1][x].state = MSS
                    Board[end+1][x].value = 0

            sunkLength = abs(start-end)
            Ships.remove(sunkLength)
            if len(Ships)==0:
                GameOver==True
        else:
            print("ERROR: Invalid Axis!")
            recordShot()
    else:
        print("ERROR! Invalid result!")
        recordShot()



# MAIN

printBoard(True) #DEBUG

while not GameOver:
    calibrate()
    printBoard(False)
    printBoard(True)
    recordShot()