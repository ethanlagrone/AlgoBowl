#Throw random helper functions in here

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