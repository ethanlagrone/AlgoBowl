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
        W = random.randint(10,15)
        NumRows = random.randint(60,90)
        NumCols = random.randint(60,90)
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
        if(Validater.horseCanEscape(G)):
            flag = False
        else:
            print("Invalid input")
    
        
    print("Done")


test()