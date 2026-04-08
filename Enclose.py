import networkx as nx
import Helper
import CreateGraph
import Validater
import random


def getNodeDistancesEromExit(G):
    exitNode = ("exit", -1, -1, 0)
    lengths = nx.single_source_shortest_path_length(G, exitNode)
    return lengths

def encloseHorse(maze, wallCount, portalPairCoords, offSet):
    #Clear walls and create graph 
    maze = Helper.clearWalls(maze)
    G = CreateGraph.createGraph(maze, portalPairCoords)
    distances = getNodeDistancesEromExit(G)
    
    exitNode = ("exit", -1, -1, 0)
    startNode = ("start", -1, -1, 0)
    capacityGraph = nx.DiGraph()

    idToTuple = {}

    #Creating a directed flow graph
    for node in G.nodes():
        if(node == startNode or node == exitNode):
            element = node[0]
            #infinite flow for start and end
            capacityGraph.add_edge(f"{node}In", f"{node}Out", capacity=float('inf'))

        else:
            element, i, j, val = node
            if element == '.':
                #Offset is changed in main, depending on how many walls it gives
                dist = distances.get(node, 999)
                nodeCapacity = dist ** offSet  
                capacityGraph.add_edge(f"{node}In", f"{node}Out", capacity=nodeCapacity)
                idToTuple[f"{node}In"] = node 
            else:
                capacityGraph.add_edge(f"{node}In", f"{node}Out", capacity=float('inf'))

        #add edges to neighbors
        for neighbor in G.neighbors(node):
            capacityGraph.add_edge(f"{node}Out", f"{neighbor}In", capacity=float('inf'))

    source = f"{startNode}In"
    sink = f"{exitNode}Out"
    
    #Get choke point
    cutValue, (reachable, nonReachable) = nx.minimum_cut(capacityGraph, source, sink)

    #Create an array where it gives us tuples of where to place walls(handled in main and Helper)
    wallsToPlace = []
    for u, v in capacityGraph.edges():
        if u in reachable and v in nonReachable:
            if "In" in u and "Out" in v:
                originalNode = idToTuple.get(u)
                if originalNode:
                    wallsToPlace.append((originalNode[1], originalNode[2]))
                
    return wallsToPlace