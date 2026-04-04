#Throw random helper functions in here

def isOnEdge(i,j,maze):
    if(i == 0 or (i == len(maze)-1) or j == 0 or (j ==len(maze[i])-1)):
        return True
    return False


def printMaze(maze):
    for row in maze:
        print()
        for element in row:
            print(element, end="")