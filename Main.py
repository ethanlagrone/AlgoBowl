import InputParser
import Validater
import GenerateRandomInput
import random
import CreateGraph
import Enclose

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
    graph = CreateGraph.createGraph(WallCount,Maze,PortalPairCoords)

    #check that input is valid(horse needs to be able to reach the outside)
    validation = Validater.validate(ourSolution)
    if(validation != "Invalid"):
        print("Horse already trapped")
        exit(1)

    #Craft our solution
    #startNode = ('start',-1,-1)
    ourSolution = Enclose.encloseHorse(graph)

    #check that solution is valid
    validation = Validater.validate(ourSolution)

    #print score and our graph
    if(validation == "Invalid"):
        print("Incorrect or invalid solution")
    else:
        print(validation)
        print(ourSolution)



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


test()
#standard()