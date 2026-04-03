"""
TODO: 
-Check that horse is enclosed
    -Can't get out(including portal paths)
-Check that the score is correct
    -Bees (-4)
    -Cherries (+4)
    -Apples (+11)
    -Grass (+1)
    -Horse tile (+1)
    -Portal tiles (+1)
-Check that no wall has been placed on a non-grass tile
"""

import networkx as nx

def validate(graph):
    startNode = ('start',-1,-1,0)
    reachable = nx.node_connected_component(graph, startNode)
    total = 0
    print(reachable)
    for node in reachable:
        thing,i,j,value = node
        total+=value

    return total

