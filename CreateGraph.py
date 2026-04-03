import networkx as nx

"""
TODO:
Create a function that creates a graph that accurately models the problem

i-1 = north
i+1 = south
j+1 = east
j-1 = west
"""

def createGraph(wallCount, maze, portalPairCoords):
    #Im thinking undireceted?

    #all elements in this array are connectable
    connectable = ['.','H','a','b','c','p']

    G = nx.Graph()


    #create all nodes format: (element, i coordinate, j coordinate)
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            node = (maze[i][j], i, j)
            if node not in G:
                G.add_node(node)



    for i in range(len(maze)):
        for j in range(len(maze[i])):
            mainElement = maze[i][j]
            mainNode = (mainElement,i,j)
                
            if(mainElement not in connectable):
                continue
            
            #connect portals
            if(mainElement == 'p'):
                for pair in portalPairCoords:
                    portal1, portal2 = pair
                    i, j = portal2
                    portalNode = ('p',i,j)
                    G.add_edge(mainNode,portalNode)


            #north edge
            if(i != 0):
                current = maze[i-1][j]
                if(current not in connectable):
                    continue
                currentNode = (current, i-1,j)
                G.add_edge(mainNode, currentNode)

            #south edge
            if(i+1 != len(maze)):
                current = maze[i+1][j]
                if(current not in connectable):
                    continue
                currentNode = (current, i+1, j)
                G.add_edge(mainNode, currentNode)

            #east edge
            if(j+1 != len(maze[i])):
                current = maze[i][j+1]
                if(current not in connectable):
                    continue
                currentNode = (current, i, j+1)
                G.add_edge(mainNode, currentNode)
            
            #west edge
            if(j != 0):
                current = maze[i][j-1]
                if(current not in connectable):
                    continue
                currentNode = (current, i, j-1)
                G.add_edge(mainNode, currentNode)


    return G