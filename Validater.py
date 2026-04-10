import networkx as nx

def score(graph):
    startNode = ('start',-1,-1,0)
    reachable = nx.node_connected_component(graph, startNode)
    total = 0

    for node in reachable:
        thing,i,j,value = node
        if(thing == 'exit'):
            return -1
        total+=value

    return total


def horseCanEscape(graph):
    startNode = ('start',-1,-1,0)
    reachable = nx.node_connected_component(graph, startNode)
    for node in reachable:
        thing,i,j,value = node
        if(thing == 'exit'):
            return True
    return False

