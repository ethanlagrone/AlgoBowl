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
    maze = Helper.clearWalls(maze)
    G = CreateGraph.createGraph(maze, portalPairCoords)
    distances = getNodeDistancesEromExit(G)
    
    exitNode = ("exit", -1, -1, 0)
    startNode = ("start", -1, -1, 0)
    capacityGraph = nx.DiGraph()

    id_to_tuple = {}

    for node in G.nodes():
        if node == startNode or node == exitNode:
            element = node[0]
            capacityGraph.add_edge(f"{node}_in", f"{node}_out", capacity=float('inf'))
        else:
            element, i, j, val = node
            if element == '.':
                dist = distances.get(node, 999)
                nodeCapacity = dist ** offSet  
                capacityGraph.add_edge(f"{node}_in", f"{node}_out", capacity=nodeCapacity)
                id_to_tuple[f"{node}_in"] = node # Save the mapping
            else:
                capacityGraph.add_edge(f"{node}_in", f"{node}_out", capacity=float('inf'))

        for neighbor in G.neighbors(node):
            capacityGraph.add_edge(f"{node}_out", f"{neighbor}_in", capacity=float('inf'))

    source = f"{startNode}_in"
    sink = f"{exitNode}_out"
    
    cut_value, (reachable, non_reachable) = nx.minimum_cut(capacityGraph, source, sink)

    wallsToPlace = []
    for u, v in capacityGraph.edges():
        if u in reachable and v in non_reachable:
            if "_in" in u and "_out" in v:
                original_node = id_to_tuple.get(u)
                if original_node:
                    wallsToPlace.append((original_node[1], original_node[2]))
                
    return wallsToPlace