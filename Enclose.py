import networkx as nx
import Helper
import CreateGraph
import Validater
import random
import numpy as np
import copy

def encloseHorse(maze, wallCount, portalPairCoords):
    original_maze = copy.deepcopy(maze)
    max_score = -np.inf
    solution = None
    for x in range(0,12):
        test_maze = copy.deepcopy(original_maze)
        for i in range(len(test_maze)):
            for j in range(len(test_maze[i])):
                current = test_maze[i][j]
                if current == 'W':
                    test_maze[i][j] = '.'
        print(f'starting x = {x}')
        result = min_cut(original_maze, test_maze, wallCount, portalPairCoords, x)
        if result is None:
            continue
        score = 0
        new_maze, S_nodes, T_nodes, walls_used = result
        if walls_used > wallCount:
            continue
        print("calculating score")
        G = CreateGraph.createGraph(wallCount, new_maze, portalPairCoords)
        score = Validater.score(G)
        print(score)
        if score > max_score:
            max_score = score
            solution = new_maze
        print(f'ending x = {x}')
    
    return solution

def min_cut(original_maze, new_maze, wallCount, portalPairCoords, x):
    # get initial wall locations so we can reconstruct input if algorithm fails
    initialWalls = []
    
    # create directed graph for flow network, add source and sink nodes
    # source = outside, sink = enclosure
    flowGraph = nx.DiGraph()
    S = "SOURCE"
    T = "SINK"
    flowGraph.add_node(S)
    flowGraph.add_node(T)

    ## FIRST LOOP: add all non-water spaces to graph
    for i in range(len(new_maze)):
        for j in range(len(new_maze[i])):
            current = new_maze[i][j]
            
            if current != '#':
                # all spaces have in and out nodes that will allow the placement of walls to be represented by flow
                node_in = (i, j, "in")
                node_out = (i, j, "out")
                flowGraph.add_node(node_in)
                flowGraph.add_node(node_out)

                if current == '.':
                    flowGraph.add_edge(node_in, node_out, capacity = 1 + x)         # capacity of 1 to represent placing one wall on this space
                else:
                    flowGraph.add_edge(node_in, node_out, capacity = np.inf)    # infinite capacity, walls cannot be placed here
                
                value = Helper.getValue(current)
                if value > 0:
                    flowGraph.add_edge(S, node_in, capacity = value)
                else:
                    flowGraph.add_edge(node_out, T, capacity = -value)

                # spaces that connect to the outside are connected to the source
                if Helper.isOnEdge(i, j, new_maze):
                    flowGraph.add_edge(S, node_in, capacity = np.inf)
                
                # force horse to be included in the sink nodes, i.e. guarantee it is in the enclosure
                if current == 'H':
                    flowGraph.add_edge(node_out, T, capacity = np.inf)

    ## SECOND LOOP: add movement edges to all neighboring nodes
    for i in range(len(new_maze)):
        for j in range(len(new_maze[i])):
            node_out = (i, j, "out")
            if i > 0 and new_maze[i-1][j] != '#':
                neighbor_node_in = (i-1, j, "in")
                flowGraph.add_edge(node_out, neighbor_node_in, capacity = np.inf)
            if j < len(new_maze[i]) - 1 and new_maze[i][j+1] != '#':
                neighbor_node_in = (i, j+1, "in")
                flowGraph.add_edge(node_out, neighbor_node_in, capacity = np.inf)
            if i < len(new_maze) - 1 and new_maze[i+1][j] != '#':
                neighbor_node_in = (i+1, j, "in")
                flowGraph.add_edge(node_out, neighbor_node_in, capacity = np.inf)
            if j > 0 and new_maze[i][j-1] != '#':
                neighbor_node_in = (i, j-1, "in")
                flowGraph.add_edge(node_out, neighbor_node_in, capacity = np.inf)

    ## THIRD LOOP: add edges between portal spaces
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
    
    cut_value, (S_nodes, T_nodes) = nx.minimum_cut(flowGraph, S, T)

    walls_to_add = []
    for i in range(len(new_maze)):
        for j in range(len(new_maze[i])):
            current = new_maze[i][j]
            if current == '.':
                node_in = (i, j, "in")
                node_out = (i, j, "out")
                if node_in in S_nodes and node_out in T_nodes:
                    walls_to_add.append((i,j))

    print(len(walls_to_add))
    if len(walls_to_add) > wallCount:
        return None
    else:
        final_maze = copy.deepcopy(original_maze)

        for i in range(len(final_maze)):
            for j in range(len(final_maze[i])):
                if final_maze[i][j] == 'W':
                    final_maze[i][j] = '.'

        for (i,j) in walls_to_add:
            final_maze[i][j] = 'W'
    
    return final_maze, S_nodes, T_nodes, len(walls_to_add)
            

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