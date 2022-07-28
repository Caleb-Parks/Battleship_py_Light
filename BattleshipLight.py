print("Hunt begins.")

WTR="_"
HIT="H"
MSS="*"
SNK="S"
SRCH="SR"#Search for ships via lattice
SINK="SK"#Sink hit ships
LATTICE_WGT = 1 # Weight of lattice pattern
KILLBOX_WGT = 5 # Weight of killbox pattern
SHIP_LENGTHS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


class Ship:
    def __init__(self, len):
        self.length = len
        self.isSunk = False
ShipList = []
for s in SHIP_LENGTHS:
    ShipList.append(Ship(s))

class Spot:
    def __init__(self, xCord:int, yCord:int):
        self.state = WTR
        self.val = 0
        self.x = xCord
        self.y = yCord
Board = []
for col in range (0, 10):
    c = []
    for row in range (0, 10):
        c.append(Spot(col, row))
    Board.append(c)


GameOver = False
TargetList = []
LastHit = (-1,-1)
Mode = SRCH


def fire(s:Spot):
    result = input("Shoot at ",s.x,s.y,": ", sep="")
    if result!=HIT and result!=MSS:
        print("ERROR")
        return fire(s)
    else:
        Board[x][y].state=result
        Board[x][y].val=0
        return result==HIT

def inBounds(s:Spot):
    return s.x>=0 and s.x<=9 and s.y>=0 and s.y<=9


def buildLattice(seekSize: int):
    for x, col in enumerate(Board):
        for y, spt in enumerate(col):
            if spt.state==WTR and (x+y)%seekSize==0: # if (RowIndex+ColIndex)%shipLength==0 : then part of target matrix (0-based) sum of the row and column indices and check if they’re divisible by five. If they are, the square is in our shot pattern. We can generalize this idea to any ship length.
                spt.val = spt.val + LATTICE_WGT
                TargetList.append(spt)

def buildKillZone(x:int, y:int):
    if inBounds(x, y-1) and Board[x][y-1].state==WTR:
        TargetList.append((x, y-1, KILLBOX_WGT))
    
    for y, line in enumerate(Board):
        for x, spt in enumerate(line):
            if spt.state==WTR and (x+y)%seekSize==0: # if (RowIndex+ColIndex)%shipLength==0 : then part of target matrix (0-based) sum of the row and column indices and check if they’re divisible by five. If they are, the square is in our shot pattern. We can generalize this idea to any ship length.
                TargetList.append((x, y, LATTICE_WGT))





# MAIN

while not GameOver:
    
    if Mode==SRCH:
        if TargetList==[]:
            buildLattice(ShipList[0].length)
        current = TargetList.pop(0)
        if fire(current[0], current[1]): # If shot is hit
            LastHit = current
            Mode==SINK
            TargetList=[]

    elif Mode==SINK:
        if TargetList==[]:
            buildKillZone(LastHit[0], LastHit[1])
        current = TargetList.pop(0)
        if fire(current[0], current[1]): # If shot is hit
            LastHit = current
            Mode==SINK
            TargetList=[]
        
        print(targetList)
        gameOver = True

    Board[1][1].state = "H" # DEBUG

    for x, col in enumerate(Board):
        for y, row in enumerate(col):
            if row.state=="H":
                targetList.append((x, y, 0)) # WORKHERE




# if (RowIndex+ColIndex)%shipLength==0 : then part of target matrix (0-based) sum of the row and column indices and check if they’re divisible by five. If they are, the square is in our shot pattern. We can generalize this idea to any ship length.