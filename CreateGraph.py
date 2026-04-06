import networkx as nx


def getValue(c):
    if c == 'a':
        return 11
    elif c == 'b':
        return -4
    elif c == 'c':
        return 4
    else:
        return 1


def createGraph(wallCount, maze, portalPairCoords):

    #all elements in this array are connectable
    connectable = ['.','H','a','b','c','p']


    exitNode = ("exit", -1, -1, 0)
    startNode = ("start", -1, -1, 0)


    G = nx.Graph()


    #create all nodes format: (element, i coordinate, j coordinate)
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            value = getValue(maze[i][j])
            node = (maze[i][j], i, j, value)
            if node not in G:
                G.add_node(node)

    G.add_node(exitNode)
    G.add_node(startNode)

    #Create all edges between nodes including between portals
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            mainElement = maze[i][j]
            value = getValue(mainElement)
            mainNode = (mainElement,i,j,value)
                
            if(mainElement not in connectable):
                continue
            
            #connect portals
            if(mainElement == 'p'):
                for pair in portalPairCoords:
                    portal1, portal2 = pair
                    x, y = portal2
                    portalNode = ('p',x,y,1)
                    G.add_edge(mainNode,portalNode)

            #make start node connected to horse
            if(mainElement == 'H'):
                G.add_edge(mainNode, startNode)


            #north edge
            if(i != 0):
                current = maze[i-1][j]
                if(current in connectable):
                    value = getValue(current)
                    currentNode = (current, i-1,j, value)
                    G.add_edge(mainNode, currentNode)

            #south edge
            if(i+1 != len(maze)):
                current = maze[i+1][j]
                if(current in connectable):
                    value = getValue(current)
                    currentNode = (current, i+1,j, value)
                    G.add_edge(mainNode, currentNode)

            #east edge
            if(j+1 != len(maze[i])):
                current = maze[i][j+1]
                if(current in connectable):
                    value = getValue(current)
                    currentNode = (current, i,j+1, value)
                    G.add_edge(mainNode, currentNode)
            
            #west edge
            if(j != 0):
                current = maze[i][j-1]
                if(current in connectable):
                    value = getValue(current)
                    currentNode = (current, i,j-1, value)
                    G.add_edge(mainNode, currentNode)

            #exits
            if(i == 0 or (i == len(maze)-1) or j == 0 or (j ==len(maze[i])-1)):
                G.add_edge(mainNode, exitNode)

    return G




def createWallGraph(wallCount, maze, portalPairCoords):

    #all elements in this array are connectable
    connectable = ['.','H','a','b','c','p']



    exitNode = ("exit", -1, -1, 0)
    startNode = ("start", -1, -1, 0)
    


    G = nx.Graph()


    #create all nodes format: (element, i coordinate, j coordinate)
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            value = getValue(maze[i][j])
            node = (maze[i][j], i, j, value)
            if node not in G:
                G.add_node(node)

    G.add_node(exitNode)
    G.add_node(startNode)

    #Create all edges between nodes including between portals
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            mainElement = maze[i][j]
            value = getValue(mainElement)
            mainNode = (mainElement,i,j,value)
                
            if(mainElement not in connectable and mainElement != 'W'):
                continue
            
            #connect portals
            if(mainElement == 'p'):
                for pair in portalPairCoords:
                    portal1, portal2 = pair
                    x, y = portal2
                    portalNode = ('p',x,y,1)
                    G.add_edge(mainNode,portalNode)

            #make start node connected to horse
            if(mainElement == 'H'):
                G.add_edge(mainNode, startNode)

            if(mainElement == 'W'):
                wallExit = ("wall",i,j,0)
                G.add_edge(mainNode, wallExit)
                continue


            #north edge
            if(i != 0):
                current = maze[i-1][j]
                if(current in connectable):
                    value = getValue(current)
                    currentNode = (current, i-1,j, value)
                    G.add_edge(mainNode, currentNode)

            #south edge
            if(i+1 != len(maze)):
                current = maze[i+1][j]
                if(current in connectable):
                    value = getValue(current)
                    currentNode = (current, i+1,j, value)
                    G.add_edge(mainNode, currentNode)

            #east edge
            if(j+1 != len(maze[i])):
                current = maze[i][j+1]
                if(current in connectable):
                    value = getValue(current)
                    currentNode = (current, i,j+1, value)
                    G.add_edge(mainNode, currentNode)
            
            #west edge
            if(j != 0):
                current = maze[i][j-1]
                if(current in connectable):
                    value = getValue(current)
                    currentNode = (current, i,j-1, value)
                    G.add_edge(mainNode, currentNode)

            #exits
            if(i == 0 or (i == len(maze)-1) or j == 0 or (j ==len(maze[i])-1)):
                G.add_edge(mainNode, exitNode)

    return G