import InputParser
import Validater
import GenerateRandomInput
import random
import CreateGraph
import Enclose
import sys


def test():
    flag = True
    while(flag == True):
        W = random.randint(1,15)
        NumRows = random.randint(10,20)
        NumCols = random.randint(10,20)
        GenerateRandomInput.ValidInput("newText.txt",W,NumRows,NumCols)

        #take in input
        with open("newText.txt", "r") as f:
            sys.stdin = f
            inputValidity = InputParser.inputParser()
        sys.stdin = sys.__stdin__ 


        #check for validity
        if(inputValidity == "Invalid"):
            continue
        
        WallCount, Maze, PortalPairCoords = inputValidity
            

        G = CreateGraph.createGraph(WallCount,Maze,PortalPairCoords)
        total = Validater.validate(G)
        if(total == -1):
            flag = False
        else:
            print("Invalid input\nTotal = " + str(total))
    
        
    print("Done")


test()