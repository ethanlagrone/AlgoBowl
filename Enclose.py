import networkx as nx
import Helper
import CreateGraph
import Validater
import random

"""
Honestly open to scraping this now :(
"""

def recursiveEncloseHorse(G, maze, walls, path, horseCoords, wallCount, portalPairCoords):
    #pretty sure this is optimal not taking into account bees and given enough walls
    #another strategy will be needed to help this increase the number of exits covered by each wall if this doesn't solve
    exitNode = ("exit", -1, -1, 0)
    startNode = ("start", -1, -1, 0)
    grassNodes = []
    possibleWallsOnPath = []
    distance = float('inf')
    furthestNode = None
    for node in path:
        element,i,j,value = node
        if(element == '.'):
            grassNodes.append(node)

    #base case
    if(walls == wallCount):
        return maze, walls, grassNodes
    
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
        if(nextDistance < distance):
            distance = nextDistance
            furthestNode = (i,j)

    if furthestNode is None:
        return maze, walls+1, grassNodes
    x,y = furthestNode
    node = (maze[x][y],x,y,Helper.getValue(maze[x][y]))
    maze[x][y] = 'W'
    walls += 1
    grassNodes.remove(node)
    G = CreateGraph.createGraph(wallCount, maze, portalPairCoords)
    try:
        path = nx.dijkstra_path(G, startNode, exitNode)
    except nx.NetworkXNoPath:
        return maze, walls, []
    return recursiveEncloseHorse(G, maze, walls, path, horseCoords, wallCount, portalPairCoords)

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
        G = CreateGraph.createGraph(wallCount, maze, portalPairCoords)


        #This gives a minimum solution that should work for everything?
        path = nx.dijkstra_path(G, startNode, exitNode)
        maze, walls, grassNodes = recursiveEncloseHorse(G, maze, walls, path, horseCoords, wallCount, portalPairCoords)
        G = CreateGraph.createGraph(wallCount, maze, portalPairCoords)

        """
        Here we need to give a mze but expand the graph as much as possible"""

        if(not Validater.horseCanEscape(G)):
            return maze 
        elif(walls > wallCount):
            print("Too many walls brother")
            return maze
        else:
            path = nx.dijkstra_path(G, startNode, exitNode)
            print("Path that breaks the answer: ")
            for element in path:
                print(str(element), end=" ")
            exit(1)
        


            


    