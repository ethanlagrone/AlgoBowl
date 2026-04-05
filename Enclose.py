import networkx as nx
import Helper
import CreateGraph
import Validater
import random

"""
TODO:
Make a function that optimally encloses the horse
Make a base case
"""
def optimize(maze):
    """
    New idea, the recursiveEncloseHorse is greedy but doesn't always have the needed wall count
    So, we run dijkstras to all the walls and find the node that could get us walls back, remove the walls that are now isolated, 
    place the new one,a nd then run recursive again with walls = however many walls we now have"""
    return 0


def recursiveEncloseHorse(G, maze, walls, path, horseCoords):
    grassNodes = []
    possibleWallsOnPath = []
    distance = float('-inf')
    furthestNode = None
    for node in path:
        element,i,j,value = node
        if(element == '.'):
            grassNodes.append(node)

    minDegree = float('inf')
    for n in grassNodes:
        if G.degree[n] < minDegree:
            minDegree = G.degree[n]

    leastConnected = []
    for n in grassNodes:
        if G.degree[n] == minDegree:
            leastConnected.append(n)

    for node in leastConnected:
        element, i, j, value = node
        if maze[i][j] == '.':
            possibleWallsOnPath.append((i, j))
    
    for i,j in possibleWallsOnPath:
        nextDistance = Helper.getDistance(horseCoords, (i,j))
        if(nextDistance > distance):
            distance = nextDistance
            furthestNode = (i,j)

    if furthestNode is None:
        return maze, walls+1, grassNodes
    x,y = furthestNode
    node = (maze[x][y],x,y,Helper.getValue(maze[x][y]))
    maze[x][y] = 'W'
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
    exitNode = ("exit", -1, -1, 0)
    startNode = ("start", -1, -1, 0)

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
        #rounds of recursion
        rounds = wallCount
        G = CreateGraph.createGraph(wallCount, maze, portalPairCoords)


        while(True):
            rounds -= 1
            path = nx.dijkstra_path(G, startNode, exitNode)
            maze, walls, grassNodes = recursiveEncloseHorse(G, maze, walls, path, horseCoords)
            G = CreateGraph.createGraph(wallCount, maze, portalPairCoords)

            
            if(not Validater.horseCanEscape(G)):
                return maze 
            if(rounds <= 0):
                path = nx.dijkstra_path(G, startNode, exitNode)
                print("Path that breaks the answer: ")
                for element in path:
                    print(str(element), end=" ")
                exit(1)
            if(walls >= wallCount):
                print("Too many walls brother")
                return maze


            


    