import networkx as nx
import Helper
import CreateGraph
import Validater

"""
TODO:
Make a function that optimally encloses the horse
"""
def optimize(maze):
    #recursively try to optimize the maze(ie. push walls back one and ensure horse cannot escape)
    return 0

def recursiveEncloseHorse(G, maze, walls, grassNodes):
    #Source: https://stackoverflow.com/questions/44532952/find-number-of-connected-edges-to-a-node-and-node-with-max-connected-edges 
    G.degree()
    leastConnected = min(grassNodes, key=lambda n: G.degree[n])
    node = leastConnected 
    element,i,j, value = node
    if(maze[i][j] == '.'):
        maze[i][j] = 'W'
        walls += 1
        grassNodes.remove(node)
        return maze, walls, grassNodes

def encloseHorse(maze, wallCount, portalPairCoords):
    changable = ['.', 'W']
    changableNodes = []
    outsideHoles = []
    outsideHoleCount = 0
    walls = 0
    grassNodes = []

    #Find all the nodes that we can change to trap the horse 
    #also count how many holes are on the outside
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            current = maze[i][j]
            if(current == 'W'):
                maze[i][j] = '.'
            if(current == 'H'):
                horseCoords = (i,j)                    
            if(current in changable):
                changableNodes.append((current,i,j))
                if(Helper.isOnEdge(i,j,maze)):
                    outsideHoleCount += 1
                    outsideHoles.append((current,i,j))

    #Check if we can trap the horse optimally off the bat
    if(wallCount >= outsideHoleCount):
        for type,i,j in outsideHoles:
            maze[i][j] = 'W'
        G = CreateGraph.createGraph(wallCount, maze, portalPairCoords)
        if(Validater.horseCanEscape(G)):
            print("Bad error, horse can escape even after encloseHorse()")
        else:
            return maze
    else:
        #trap horse, then recursively expand
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                current = maze[i][j]
                if(current == 'W'):
                    maze[i][j] = '.'
                if(current == 'H'):
                    horseCoords = (i,j)  
                if(current == '.'):
                    grassNodes.append(('.',i,j,1))  
        
        G = CreateGraph.createGraph(wallCount, maze, portalPairCoords)
        while(True):
            maze, walls, grassNodes = recursiveEncloseHorse(G, maze, walls, grassNodes)
            G = CreateGraph.createGraph(wallCount, maze, portalPairCoords)
            if(not Validater.horseCanEscape(G)):
                return maze 
            if(walls >= wallCount):
                print("Too many walls brother")
                return maze


            


    