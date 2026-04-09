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


    #connect portals
    for pair in portalPairCoords:
        portal1, portal2 = pair
        i,j = portal1
        portal1Node = ('p', i,j, 1) 
        x, y = portal2
        portal2Node = ('p',x,y,1)
        G.add_edge(portal1Node,portal2Node)


    #Create all edges between nodes in North, South, East, West directions
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            mainElement = maze[i][j]
            value = getValue(mainElement)
            mainNode = (mainElement,i,j,value)
                
            if(mainElement not in connectable):
                continue
            
            

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


def addWall(G, wallLocation):
    i,j = wallLocation
    nodeToRemove = ('.',i,j,1)
    G.remove_node(nodeToRemove)


def removeWallFromGraph(G, wallLocation, maze):
    i,j = wallLocation
    mainNode = ('.',i,j,1)
    connectable = ['.','H','a','b','c','p']
    exitNode = ("exit", -1, -1, 0)

    G.add_node(mainNode)

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

    if(i == 0 or (i == len(maze)-1) or j == 0 or (j ==len(maze[i])-1)):
                G.add_edge(mainNode, exitNode)





def createWalledGraph(wallCount, maze, portalPairCoords):
    #THIS WILL BE  A DIRECTED GRAPH AS WHEN THEY ACCESS WALLS THEY CAN'T GO BACK
    #all elements in this array are connectable
    connectable = ['.','H','a','b','c','p']



    exitNode = ("exit", -1, -1, 0)
    startNode = ("start", -1, -1, 0)
    


    G = nx.DiGraph()


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
                G.add_edge(startNode, mainNode)

            if(mainElement == 'W'):
                generalWallExit = ("wall",-1,-1,0)
                wallExit = ("wall",i,j,0)
                G.add_node(wallExit)
                G.add_edge(mainNode, wallExit)
                G.add_edge(wallExit, generalWallExit)
                #North edge, one way into walls
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



            #north edge
            if(i != 0):
                current = maze[i-1][j]
                if(current in connectable):
                    value = getValue(current)
                    currentNode = (current, i-1,j, value)
                    G.add_edge(mainNode, currentNode)
                    G.add_edge(currentNode, mainNode)

            #south edge
            if(i+1 != len(maze)):
                current = maze[i+1][j]
                if(current in connectable):
                    value = getValue(current)
                    currentNode = (current, i+1,j, value)
                    G.add_edge(mainNode, currentNode)
                    G.add_edge(currentNode, mainNode)

            #east edge
            if(j+1 != len(maze[i])):
                current = maze[i][j+1]
                if(current in connectable):
                    value = getValue(current)
                    currentNode = (current, i,j+1, value)
                    G.add_edge(mainNode, currentNode)
                    G.add_edge(currentNode, mainNode)
            
            #west edge
            if(j != 0):
                current = maze[i][j-1]
                if(current in connectable):
                    value = getValue(current)
                    currentNode = (current, i,j-1, value)
                    G.add_edge(mainNode, currentNode)
                    G.add_edge(currentNode, mainNode)

            #exits
            if(i == 0 or (i == len(maze)-1) or j == 0 or (j ==len(maze[i])-1)):
                G.add_edge(mainNode, exitNode)
        
    return G