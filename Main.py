import InputParser
import Validater
import GenerateRandomInput
import random
import CreateGraph
import Enclose
import OutputParser
import Helper

"""
TODO:
-CreateGraph.py
-Enclose.py
-Validater.py
"""

#THIS WILL GO START TO FINISH, VALIDATING AN OUTPUT, CREATING A SOLUTION, VALIDATING IT, AND OUTPUTTING THE RESULT
def standard():
    #take in input
    inputValidity = InputParser.inputParser()

    #check for validity
    if(inputValidity == "Invalid"):
        print("Invalid input")
        exit(1)
    else:
        WallCount, Maze, PortalPairCoords = inputValidity

    #create graph from input
    graph = CreateGraph.createGraph(Maze,PortalPairCoords)

    #check that input is valid(horse needs to be able to reach the outside)
    """if(Validater.horseCanEscape(graph)):
        print("Horse not trapped")
        exit(1)
    """
    #Craft our solution
    #startNode = ('start',-1,-1)
    #returning a maze
    offSet = 2
    while(True):
        wallsToPlace = Enclose.encloseHorse(Maze, WallCount,PortalPairCoords, offSet)
        #print(wallsToPlace)
        #print(len(wallsToPlace), WallCount)
        if(len(wallsToPlace) > WallCount):
            offSet -= .1
        else:
            break
    ourSolution = Helper.placeWalls(Maze, wallsToPlace)
    #Helper.printMaze(ourSolution)
    if(not OutputParser.outputParser(Maze, ourSolution, WallCount)):
        print("Output and input maze don't match")
        exit(1)
    #check that solution is valid
    validation = Validater.score(CreateGraph.createGraph(ourSolution, PortalPairCoords))

    
    #print score and our graph
    if(validation == -1):
        print("Incorrect or invalid solution")
        Helper.printMaze(ourSolution)
    else:
        print(validation, end=" ")
        Helper.printMaze(ourSolution)


#DO WHAT YOU NEED HERE
def test():
    #take in input
    inputValidity = InputParser.inputParser()

    #check for validity
    if(inputValidity == "Invalid"):
        print("Invalid input")
        exit(1)
    else:
        WallCount, Maze, PortalPairCoords = inputValidity
        

    G = CreateGraph.createGraph(WallCount,Maze,PortalPairCoords)
    total = Validater.validate(G)
    if(total == -1):
        print("Valid Input")
    else:
        print("Invalid input\nTotal = " + str(total))


#test()
standard()