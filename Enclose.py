import networkx as nx
import Helper
import CreateGraph
import Validater
import random

"""
New and better idea, start by using dijkstras to find a minimum viable solution
Then push out and optimize
"""

def expand():
    """
    TODO:
    Given a maze and whatever else, you maximize the amount of space the horse is covering
    """
    return 0

def testIfWallCreatesRedundancies(wallCount, wall, maze, portalPairCoords):
    #Given a wall, test to see if it may create redundancies
    i, j = wall
    old = maze[i][j]
    maze[i][j] = 'W'
    redundantWalls = Helper.getRedundantWalls(maze, wallCount, portalPairCoords)
    maze[i][j] = old

    if redundantWalls and len(redundantWalls) >= 1:
        return redundantWalls
    return None


def optimize(maze, wallCoords, wallCount, portalPairCoords, horseCoords):
    print("Running optimize")
    """
    Old idea, the recursiveEncloseHorse is greedy but doesn't always have the needed wall count
    So, we run dijkstras to all the walls and find the node that could get us walls back, remove the walls that are now isolated, 
    place the new one,a nd then run recursive again with walls = however many walls we now have
    """
    startNode = ("start", -1, -1, 0)
    allPaths = []
    nodeAppearence = dict()
    exitNode = ("exit", -1, -1, 0)
    freedWalls = 0
    redundantWalls = []

    
    #Check if after running recursiveEncloseHorse if there are redundant walls, if there are, update ir
    redundantWalls = Helper.getRedundantWalls(maze, wallCount, portalPairCoords)
    if(len(redundantWalls) > 0):
        for i,j in redundantWalls:
            maze[i][j] = '.'
            freedWalls += 1
        G=CreateGraph.createGraph(wallCount,maze, portalPairCoords)
        try:
            path = nx.dijkstra_path(G, startNode, exitNode)
        except nx.NetworkXNoPath:
            return maze, freedWalls, []
        print("Running recursiveenclose horse in eclose.py top", redundantWalls)
        maze, freedWalls, grassNodes = recursiveEncloseHorse(G, maze, freedWalls, path, horseCoords, wallCount, portalPairCoords)
        G = CreateGraph.createGraph(wallCount, maze, portalPairCoords)
        if(not Validater.horseCanEscape(G)):
            return maze, 0, []
    redundantWalls = []


    G = CreateGraph.createWalledGraph(wallCount, maze, portalPairCoords)
        

    allPaths = Helper.getWallPaths(maze, wallCount, portalPairCoords)

    #AFTER THIS WE NEED TO FIND A NODE THAT IS FURTHEST OF MIN DEGREE ON THE PATH TO OTHER WALLS

    #Find most frequently appearing nodes on the path
    nodeFrequencey = dict()
    for path in allPaths:
        for node in path:
            element, i,j, value = node
            if(element == '.'):
                if(node in nodeFrequencey):
                    nodeFrequencey[node] += 1
                else:
                    nodeFrequencey[node] = 1
    
    #Sort nodes by value and then go through them finding a node of degree 1 or 2
    # Set that as temp wall, see if any walls become redundant, then check again untill you find a spot that can make walls redundant
    G = CreateGraph.createGraph(wallCount, maze, portalPairCoords)
    sortedNodeFrequency = dict(sorted(nodeFrequencey.items(), key=lambda item: item[1], reverse=True))

    chosenWall = None
    chosenRedundantWalls = None

    for node, count in sortedNodeFrequency.items():
        degree = G.degree[node]
        if degree <= 2:
            element, i, j, val = node
            wall = (i, j)

            redundantWalls = testIfWallCreatesRedundancies(wallCount, wall, maze, portalPairCoords)

            if redundantWalls and len(redundantWalls) >= 1:
                chosenWall = wall
                chosenRedundantWalls = redundantWalls
                break

    removedWalls = 0

    if chosenWall is not None:
        i, j = chosenWall
        maze[i][j] = 'W'
        for x, y in chosenRedundantWalls:
            if (x, y) != chosenWall:
                maze[x][y] = '.'
                removedWalls += 1
    else:
        print("UH OH")
        exit(1)

    freedWalls = removedWalls - 1
    if freedWalls > 0:
        G = CreateGraph.createGraph(wallCount, maze, portalPairCoords)
        try:
            path = nx.dijkstra_path(G, startNode, exitNode)
        except nx.NetworkXNoPath:
            return maze, freedWalls, []
        print("Running recursiveenclose horse in eclose.py bottom")
        return recursiveEncloseHorse(G, maze, freedWalls, path, horseCoords, wallCount, portalPairCoords)
    else:
        return maze, 0, []

        
    
    


def recursiveEncloseHorse(G, maze, walls, path, horseCoords, wallCount, portalPairCoords):
    #pretty sure this is optimal not taking into account bees and given enough walls
    #another strategy will be needed to help this increase the number of exits covered by each wall if this doesn't solve
    exitNode = ("exit", -1, -1, 0)
    startNode = ("start", -1, -1, 0)
    grassNodes = []
    possibleWallsOnPath = []
    distance = float('-inf')
    furthestNode = None
    for node in path:
        element,i,j,value = node
        if(element == '.'):
            grassNodes.append(node)

    #base case
    if(walls == 0):
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
        if(nextDistance > distance):
            distance = nextDistance
            furthestNode = (i,j)

    if furthestNode is None:
        return maze, walls, grassNodes
    x,y = furthestNode
    node = (maze[x][y],x,y,Helper.getValue(maze[x][y]))
    maze[x][y] = 'W'
    walls -= 1
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
    walls = wallCount
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


        try:
            path = nx.dijkstra_path(G, startNode, exitNode)
        except nx.NetworkXNoPath:
            return maze
        maze, walls, grassNodes = recursiveEncloseHorse(G, maze, walls, path, horseCoords, wallCount, portalPairCoords)
        G = CreateGraph.createGraph(wallCount, maze, portalPairCoords)
        #Recursive enclose horse

        attempts = 0
        maxAttempts = wallCount
        wallCoords = Helper.getWallCoords(maze)
        while(Validater.horseCanEscape(G)):
            if(attempts > maxAttempts):
                break
            result = optimize(maze, wallCoords, wallCount, portalPairCoords, horseCoords)
            maze, walls, path = result
            G = CreateGraph.createGraph(wallCount, maze, portalPairCoords)
            wallCoords = Helper.getWallCoords(maze)
            attempts += 1
        

        if(not Validater.horseCanEscape(G)):
            return maze 
        elif(walls > wallCount):
            print("Too many walls brother")
            return maze
        else:
            try:
                path = nx.dijkstra_path(G, startNode, exitNode)
            except nx.NetworkXNoPath:
                return maze
            print("Path that breaks the answer: ")
            for element in path:
                print(str(element), end=" ")
            exit(1)
        


            


    