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
def optimize(maze, wallCords, wallCount, portalPairCoords, horseCoords):
    """
    New idea, the recursiveEncloseHorse is greedy but doesn't always have the needed wall count
    So, we run dijkstras to all the walls and find the node that could get us walls back, remove the walls that are now isolated, 
    place the new one,a nd then run recursive again with walls = however many walls we now have
    """
    startNode = ("start", -1, -1, 0)
    allPaths = []
    nodeAppearence = dict()
    G = CreateGraph.createWallGraph(wallCount, maze, portalPairCoords)
    for i,j in wallCords:
        wallExit = ("wall",i,j,0)
        try:
            path = nx.dijkstra_path(G, startNode, wallExit)
            allPaths.append(path)
        except nx.NetworkXNoPath:
            pass
    
    for array in allPaths:
        print(array)
        for node in array:
            element,i,j,val = node
            if(element == '.'):
                if(node not in nodeAppearence):
                    nodeAppearence[node] = 1
                elif(node in nodeAppearence):
                    nodeAppearence[node] += 1

    mostAppearingNode = None
    largestDistance = 0
    for node, count in nodeAppearence.items():
        print(node, count)
        element,i,j,val = node
        distance = Helper.getDistance(horseCoords,(i,j))
        degree = G.degree[node]
        if 0 < degree <= 2 and distance >= largestDistance and count >= 2:
            mostAppearingNode = node

    if mostAppearingNode is not None:
        element, i, j, val = mostAppearingNode
        maze[i][j] = 'W'
    print("Most frequent node in paths: " + str(mostAppearingNode))
    return 0


def recursiveEncloseHorse(G, maze, walls, path, horseCoords, wallCount, portalPairCoords):
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


        path = nx.dijkstra_path(G, startNode, exitNode)
        maze, walls, grassNodes = recursiveEncloseHorse(G, maze, walls, path, horseCoords, wallCount, portalPairCoords)
        G = CreateGraph.createGraph(wallCount, maze, portalPairCoords)


        #"""
        #Will be this but need to implement optimize
        wallCoords = []
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                current = maze[i][j]
                if(current == 'W'):
                    wallCoords.append((i,j))

        maxAttempts = wallCount
        attempts = 0
        while(Validater.horseCanEscape(G)):
            if(attempts > maxAttempts):
                break
            maze = optimize(maze, wallCoords, wallCount, portalPairCoords, horseCoords)
            G = CreateGraph.createGraph(wallCount, maze, portalPairCoords)
            wallCoords = []
            for i in range(len(maze)):
                for j in range(len(maze[i])):
                    current = maze[i][j]
                    if(current == 'W'):
                        wallCoords.append((i,j))
            attempts += 1
        #"""

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
        


            


    