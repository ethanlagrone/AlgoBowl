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
    T = nx.bfs_tree(graph, startNode)
    total = 0
    print(T.nodes())
    for node in T.nodes():
        thing,i,j,value = node
        total+=value

    return total

