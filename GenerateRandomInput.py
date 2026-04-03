import random


#Should always generate valid inputs
def ValidInput(filename):
    W = int(input("Give wall count for random input: "))

    #filename = "newInput.txt"

    NumCols = int(input("Give your wanted number of cols: "))
    NumRows = int(input("Give your wanted number of rows: "))

    with open(filename,"w") as file:
        file.write(str(W))


    with open(filename, "a") as file:
        file.write("\n")
        file.write(str(NumRows) + " " + str(NumCols))

    mazeTiles = ['.','H','#','W','a','b','c','p']
    maze = []
    portals = []
    horseCount = 0
    wallCount = 0


    with open(filename, "a") as file:
        for i in range(NumRows):
            maze.append([])
            current = maze[i]
            for j in range(NumCols):
                chosen = random.choice(mazeTiles)
                if(chosen == 'p'):
                    portals.append((i,j))
                if(chosen == 'H'):
                    if(horseCount == 1):
                        current.append('.')
                        continue
                if(chosen == 'W'):
                    if(wallCount >= W):
                        current.append('.')
                        continue 
                    else:
                        wallCount += 1    
                current.append(chosen)


    if(len(portals) % 2 != 0):
        fixPortalCount = random.choice(portals)
        i,j = fixPortalCount
        maze[i][j] = '.'
        portals.remove(fixPortalCount)

    with open(filename, "a") as file:
        for array in maze:
            file.write("\n")
            for element in array:
                file.write(str(element))


    with open(filename, "a") as file:
        file.write("\n")
        length = len(portals)
        length = int(length/2)
        file.write(str(length))
        for i in range(length):
            portal1 = random.choice(portals)
            portals.remove(portal1)
            portal2 = random.choice(portals)
            portals.remove(portal2)
            a,b = portal1
            i,j = portal2
            file.write("\n")
            file.write(str(a) + " " + str(b) + " " + str(i) + " " + str(j))



#Will likely have too many walls or too many horses
def LikelyNotValidInput(filename):
    W = int(input("Give wall count for random input: "))


    #filename = "newInput.txt"

    NumCols = int(input("Give your wanted number of cols: "))
    NumRows = int(input("Give your wanted number of rows: "))

    with open(filename,"w") as file:
        file.write(str(W))


    with open(filename, "a") as file:
        file.write("\n")
        file.write(str(NumRows) + " " + str(NumCols))

    mazeTiles = ['.','H','#','W','a','b','c','p']
    maze = []
    portals = []


    with open(filename, "a") as file:
        for i in range(NumRows):
            maze.append([])
            current = maze[i]
            for j in range(NumCols):
                chosen = random.choice(mazeTiles)
                current.append(chosen)


    if(len(portals) % 2 != 0):
        fixPortalCount = random.choice(portals)
        i,j = fixPortalCount
        maze[i][j] = '.'
        portals.remove(fixPortalCount)

    with open(filename, "a") as file:
        for array in maze:
            file.write("\n")
            for element in array:
                file.write(str(element))


    with open(filename, "a") as file:
        file.write("\n")
        length = len(portals)
        length = int(length/2)
        file.write(str(length))
        for i in range(length):
            portal1 = random.choice(portals)
            portals.remove(portal1)
            portal2 = random.choice(portals)
            portals.remove(portal2)
            a,b = portal1
            i,j = portal2
            file.write("\n")
            file.write(str(a) + " " + str(b) + " " + str(i) + " " + str(j))


    return