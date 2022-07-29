# from re import S


print("Hunt begins.\n")

# GLOBALS

useLattice=True
Ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

WTR=" "
HIT="H"
MSS="*"
SNK="S"

DEFAULT_WGT = 0
PSBLPOS_WGT = 1 # Weight of a possible ship position
LATTICE_WGT = 1 # Weight of lattice pattern
HUNTBOX_WGT = 100 # Weight of huntbox pattern

GameOver = False



# OBJECTS

class Spot:
    def __init__(self):
        self.state = WTR
        self.weight = DEFAULT_WGT
    def setState(self, st):
        if st=="M":
            self.state=MSS 
        elif st=="H":
            self.state=HIT
        elif st=="S":
            self.state=SNK
        elif st=="W":
            self.state=WTR
    def prntweight(self):
        if self.weight<=9:
            print(" ",int(self.weight),"  ",sep="",end="")
        elif self.weight<=99:
            print(" ",int(self.weight)," ",sep="",end="")
        else:
            print(int(self.weight)," ",sep="",end="")
    def prntState(self):
        print(" ",self.state,"  ",sep="",end="")
     
Board=[]
for col in range (0, 10):
    c = []
    for row in range (0, 10):
        c.append(Spot())
    Board.append(c)

class Hitstreak:
    def __init__(self):
        self.start = -1
        self.end = -1
        self.coord = -1
        self.isVert = False
HS = Hitstreak()



# UTIL FUNCTIONS

def inBounds(y, x):
    """Returns true if the passed spot is inside the Board's bounds"""
    return y>=0 and y<=9 and x>=0 and x<=9

def isState(y:int, x:int, st8:str):
    """Returns true if the passed spot is the passed state and is in bounds"""
    return inBounds(y, x) and Board[y][x].state==st8

def resetweights():
    """Resets all spots' weights"""
    for y, line in enumerate(Board):
        for x, spt in enumerate(line):
            spt.weight = DEFAULT_WGT

def set(y:int, x:int, st8, w8):
    """Sets the passed spot to the passed state and weight"""
    if inBounds(y,x):
        Board[y][x].state = st8
        Board[y][x].weight = w8

def addWGT(y:int, x:int, weight):
    """Increments the specified spot (must be water) by the specified weight"""
    if inBounds(y,x) and Board[y][x].state==WTR:
        Board[y][x].weight += weight

def recordSink(y:int,x:int):
    """Marks hits on a sunk ship as sunk, marks spots around sunk ship as misses"""
    set(y,x,HIT,0)
    if not (isState(y-1,x,HIT) or isState(y+1,x,HIT) or isState(y,x-1,HIT) or isState(y,x+1,HIT)):
        # (Sunk a ship of length=1)
        HS.start = x
        HS.end = x
        HS.coord = y
        HS.isVert = True
    else:
        if isState(y,x-1,HIT):
            HS.start = x-1
            HS.end = x
            HS.coord = y
            HS.isVert = False
        elif isState(y-1,x,HIT):
            HS.start = y-1
            HS.end = y
            HS.coord = x
            HS.isVert = True   
        elif isState(y,x+1,HIT):
            HS.start = x
            HS.end = x+1
            HS.coord = y
            HS.isVert = False
        elif isState(y+1,x,HIT):
            HS.start = y
            HS.end = y+1
            HS.coord = x
            HS.isVert = True  
        # Building full hitstreak:
        while True:
            if (HS.isVert and isState(HS.start-1,HS.coord,HIT)) or (not HS.isVert and isState(HS.coord,HS.start-1,HIT)):
                HS.start -= 1
            elif (HS.isVert and isState(HS.end+1,HS.coord,HIT)) or (not HS.isVert and isState(HS.coord,HS.end+1,HIT)):
                HS.end += 1
            else:
                break
    # Marking misses around sunk ship:
    for i in range(HS.start-1, HS.end+2):
        if HS.isVert:
            set(i,HS.coord,SNK,0)
            set(i,HS.coord-1,MSS,0)
            set(i,HS.coord+1,MSS,0)
        else:
            set(HS.coord,i,SNK,0)
            set(HS.coord-1,i,MSS,0)
            set(HS.coord+1,i,MSS,0)
    if HS.isVert:
        set(HS.start-1,HS.coord,MSS,0)
        set(HS.end+1,HS.coord,MSS,0)
    else:
        set(HS.coord,HS.start-1,MSS,0)
        set(HS.coord,HS.end+1,MSS,0)
    # Removing sunk ship from Ships[]:
    Ships.remove(abs(HS.end-HS.start)+1)
    # Checking for win:
    if len(Ships)==0:
        global GameOver
        GameOver=True

def huntHeuristic():
    """Searches for unsunk hits, weighting possible positions of the rest of the ship with HUNTBOX_WGT"""
    foundHit=False
    # Searches for Hit
    for y in range(0, 10):
        for x in range(0, 10):
            if isState(y,x,HIT):
                foundHit=True
                # Setting hitstreak if applicable
                if isState(y,x+1,HIT):
                    HS.start = x
                    HS.end = x+1
                    HS.coord = y
                    HS.isVert = False
                elif isState(y+1,x,HIT):
                    HS.start = y
                    HS.end = y+1
                    HS.coord = x
                    HS.isVert = True
                else:
                    # Isolated Hit, setting weights
                    addWGT(y-1,x,HUNTBOX_WGT)
                    addWGT(y+1,x,HUNTBOX_WGT)
                    addWGT(y,x-1,HUNTBOX_WGT)
                    addWGT(y,x+1,HUNTBOX_WGT)
                    continue                    
                # Building full hitstreak:
                while (HS.isVert and isState(HS.end+1,HS.coord,HIT)) or (not HS.isVert and isState(HS.coord,HS.end+1,HIT)):
                    HS.end += 1
                # Weighting spot before start of hitstreak:
                addWGT(HS.start-1,x,HUNTBOX_WGT) if HS.isVert else addWGT(y,HS.start-1,HUNTBOX_WGT)
                # Weighting spot after end of hitstreak:
                addWGT(HS.end+1,HS.coord,HUNTBOX_WGT) if HS.isVert else addWGT(HS.coord,HS.end+1,HUNTBOX_WGT)              
                return foundHit
    return foundHit

def possiblePositionsHeuristic():
    """Calculates each possible position for each ship and increments the weights of the spots in that position by PSBLPOS_WGT"""
    for length in Ships:
        for y in range(0, 10):
            for x in range(0, 10):
                x_validPlace = True
                y_validPlace = True
                for i in range(0, length):
                    if not isState(y,x+i,WTR):
                        x_validPlace=False
                    if not isState(y+i,x,WTR):
                        y_validPlace=False
                if x_validPlace:
                    for i in range(0, length):
                        addWGT(y,x+i,PSBLPOS_WGT)
                if y_validPlace:
                    for i in range(0, length):
                        addWGT(y+i,x,PSBLPOS_WGT)

def latticeHeuristic(seekSize: int):
    """Caculates and weights with LATTICE_WGT the minimum set of spots that a ship of passed size must touch"""
    for y in range(0, 10):
        for x in range(0, 10):
            if isState(y,x,WTR) and (x+y)%seekSize==0:
                addWGT(y,x,LATTICE_WGT)



# CORE FUNCTIONS

def calibrate():
    """Resets weights and then sets weights using heuristics"""
    resetweights()
    hitFound = huntHeuristic()
    if not hitFound:
        possiblePositionsHeuristic()
        if useLattice:
            latticeHeuristic(Ships[0])

def printBoard(printweights:bool):
    """Prints the board's weights if True is passed, else prints the board's states"""
    print("\n##    1   2   3   4   5   6   7   8   9   10\n")
    for y, line in enumerate(Board):
        # Line number:
        if y<9:
            print(" ",end="")
        print(y+1," [ ",sep="",end="")
        # Printing Line:
        for x, spt in enumerate(line):
            spt.prntweight() if printweights else spt.prntState()
        print("]\n") # End of line

def recordShot():
    """Records and proccesses a shot and its results"""
    x = int(input("\nX coordinate of shot: ")) - 1
    y = int(input("Y coordinate of shot: ")) - 1
    res = input("Result (H, M, or S): ")
    if res=="M":
        set(y,x,MSS,0)
    elif res=="H":
        set(y,x,HIT,0)
    elif res=="S":
        recordSink(y,x)
        


# MAIN
while not GameOver:
    calibrate()
    printBoard(False)
    printBoard(True)
    recordShot()
printBoard(False)
print("\nCongrats!")