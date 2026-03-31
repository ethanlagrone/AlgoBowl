"""• Empty grass tiles, the grass tile with the horse, and grass tiles with portals all score +1 point
• A grass tile with an apple scores +11 points (+1 for the grass tile, and +10 for the apple)
• A grass tile with bees scores −4 points (+1 for the grass tile, and −5 for the bees)
• A grass tile with cherries scores +4 points (+1 for the grass tile, and +3 for the cherries)

"""


#actually build walls
def horse():
    return 0


#BFS to check if the horse can get out
def BFS():
    return 0


#Num of walls
Line1 = input()
W= int(Line1)


#NumRows and NumCols
Line2 = input().split(" ")
NumRows = Line2[0]
NumCols = Line2[1]

Maze = []

#Actual maze input
for i in range(NumRows):
    Line = input().split()
    Maze.append(Line)



#Number of portal pairs
Line4 = input()
PP = int(Line4)

#Connecting portals
for i in range(PP):
    Line5 = input().split(" ")
    Portal1Row = Line5[0]
    Portal1Col = Line5[1]
    Portal2Row = Line5[2]
    Portal2Col = Line5[3]

