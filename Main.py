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

    #Craft our solution
    ourSolution = Enclose.encloseHorse(graph)

    #check that solution is valid
    validation = Validater.validate(ourSolution)

    #print score and our graph
    if(validation == 0):
        print("Incorrect or invalid solution")
    else:
        print(validation)
        print(ourSolution)





standard()