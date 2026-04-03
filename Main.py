#Have this file parse input
#last thing to do is to check if the horse can get out on intial map(it needs to be able to)

#Constants
mazeTiles = {'.','H','#','W','a','b','c','p'}
SIZE_LIMIT = 10**4


#Num of walls, First line of input
W = int(input())


#NumRows and NumCols, Second line of input
Line2 = input().split(" ")
NumRows, NumCols = Line2
NumRows = int(NumRows)
NumCols = int(NumCols)

if(NumRows <= 3):
    print("Too few rows")
    exit(1)
if(NumCols*NumRows > SIZE_LIMIT):
    print("Too many rows and columns")
    exit(1)


Maze = []
PortalCoordinates = []
WallCount = 0
PortalCount = 0

#Actual maze input
for i in range(NumRows):
    Line = list(input())
    if(len(Line) != NumCols):
        print("Incorrect number of columns")
        exit(1)
    for j in range(NumCols):
        char = Line[j]
        #check for chars to be usable
        if(char not in mazeTiles):
            print("Bad input")
            exit(1)  
        #Count walls to ensure there are not too many
        if(char == 'W'):
            WallCount += 1
            if(WallCount > W):
                print("Too many walls in input")
                exit(1)
        #Count portals
        if(char == 'p'):
            PortalCount += 1
            PortalCoordinates.append((i,j))
    Maze.append(Line)



#Number of portal pairs
Line4 = input()
PP = int(Line4)

#Check portal count
if(PortalCount != (2*PP)):
    print("Protal error")
    exit(1)

#Connecting portals
for i in range(PP):
    Line5 = input().split(" ")
    P1Row, P1Col, P2Row, P2Col = Line5
    portal1 = (int(P1Row), int(P1Col))
    portal2 = (int(P2Row), int(P2Col))

    #Ensure given portal coordinates match the graph
    if(portal1 not in PortalCoordinates or portal2 not in PortalCoordinates):
        print("Incorrect portal coords")
        exit(1)

print("Valid")