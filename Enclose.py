import networkx as nx
import Helper
import CreateGraph
import Validater
import random
import numpy as np

def encloseHorse(maze, wallCount, portalPairCoords):
    # get initial wall locations so we can reconstruct input if algorithm fails
    initialWalls = []
    
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            current = maze[i][j]
            if current == 'W':
                initialWalls.append((i,j))
                maze[i][j] = '.'
    
    flowGraph = nx.DiGraph()
    S = "SOURCE"
    T = "SINK"
    flowGraph.add_node(S)
    flowGraph.add_node(T)

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            current = maze[i][j]
            if current != '#':
                node_in = (i, j, "in")
                node_out = (i, j, "out")
                flowGraph.add_node(node_in)
                flowGraph.add_node(node_out)

                if current == '.':
                    flowGraph.add_edge(node_in, node_out, capacity = 1)
                else:
                    flowGraph.add_edge(node_in, node_out, capacity = np.inf)
                
                value = Helper.getValue(current)
                flowGraph.add_edge(S, node_in, capacity = value)
                flowGraph.add_edge(node_out, T, capacity = -value)

                if Helper.isOnEdge(i, j, maze):
                    flowGraph.add_edge(S, node_in, capacity = np.inf)
                
                if current == 'H':
                    flowGraph.add_edge(node_out, T, capacity = np.inf)

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            node_out = (i, j, "out")
            if i > 0 and maze[i-1][j] != '#':
                neighbor_node_in = (i-1, j, "in")
                flowGraph.add_edge(node_out, neighbor_node_in, capacity = np.inf)
            if j < len(maze[i]) - 1 and maze[i][j+1] != '#':
                neighbor_node_in = (i, j+1, "in")
                flowGraph.add_edge(node_out, neighbor_node_in, capacity = np.inf)
            if i < len(maze) - 1 and maze[i+1][j] != '#':
                neighbor_node_in = (i+1, j, "in")
                flowGraph.add_edge(node_out, neighbor_node_in, capacity = np.inf)
            if j > 0 and maze[i][j-1] != '#':
                neighbor_node_in = (i+1, j, "in")
                flowGraph.add_edge(node_out, neighbor_node_in, capacity = np.inf)

    for pair in portalPairCoords:
        p1, p2 = pair
        p1_x, p1_y = p1
        p2_x, p2_y = p2

        p1_node_in = (p1_x, p1_y, "in")
        p1_node_out = (p1_x, p1_y, "out")
        p2_node_in = (p2_x, p2_y, "in")
        p2_node_out = (p2_x, p2_y, "out")

        flowGraph.add_edge(p1_node_out, p2_node_in, capacity = np.inf)
        flowGraph.add_edge(p2_node_out, p1_node_in, capacity = np.inf)
            

### OLD SOLUTION BELOW THIS POINT ###

'''
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
'''  