#Throw random helper functions in here
import math
def isOnEdge(i,j,maze):
    if(i == 0 or (i == len(maze)-1) or j == 0 or (j ==len(maze[i])-1)):
        return True
    return False

def isOnEdgeOffset(i,j,maze,offset):
    if(i-offset == 0 or (i == len(maze)-1-offset) or j-offset == 0 or (j ==len(maze[i])-1-offset)):
        return True
    return False


def printMaze(maze):
    for row in maze:
        print()
        for element in row:
            print(element, end="")

def clearWalls(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            element = maze[i][j]
            if(element == 'W'):
                maze[i][j] = '.'


def getValue(c):
    if c == 'a':
        return 11
    elif c == 'b':
        return -4
    elif c == 'c':
        return 4
    else:
        return 1
    
def getDistance(horseCoords, node):
    distance = 0
    horseI,horseJ = horseCoords
    i,j = node

    distance += math.sqrt(((abs(horseI-i))**2) + ((abs(horseJ-j))**2))

    return distance
    

def countWalls(maze):
    count = 0
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            element = maze[i][j]
            if(element == 'W'):
                count += 1

    return count

def getWallCoords(maze):
    wallCoords = []
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            element = maze[i][j]
            if(element == 'W'):
                wallCoords.append((i,j))

    return wallCoords