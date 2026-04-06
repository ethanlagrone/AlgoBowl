import InputParser
import Validater
import GenerateRandomInput
import random
import CreateGraph
import Enclose
import sys
import Helper
import OutputParser


def test(filename):
    flag = True
    while(flag == True):
        W = random.randint(150,151)
        NumRows = random.randint(60,90)
        NumCols = random.randint(60,90)
        GenerateRandomInput.ValidInput(filename,W,NumRows,NumCols)

        #take in input
        with open(filename, "r") as f:
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
            continue
    
        
    return filename


def runMain(filename):
    outputFile = "output.txt"
    with open(filename, "r") as f:
        sys.stdin = f
        inputValidity = InputParser.inputParser()
    sys.stdin = sys.__stdin__ 

    WallCount, Maze, PortalPairCoords = inputValidity

    G = CreateGraph.createGraph(WallCount,Maze,PortalPairCoords)
    ourSolution = Enclose.encloseHorse(Maze, WallCount,PortalPairCoords)

    #check that solution is valid
    validation = Validater.score(CreateGraph.createGraph(WallCount, ourSolution, PortalPairCoords))


    #print score and our graph
    if(validation == -1):
        print("Incorrect or invalid solution")
        Helper.printMaze(ourSolution)
        return False
    else:
        if(OutputParser.outputParser(Maze,ourSolution)):
            with open(outputFile ,"w") as file:
                file.write(str(validation) +  " ")
            with open(outputFile ,"a") as file:
                for row in Maze:
                    file.write("\n")
                    for element in row:
                        file.write(element)
            return True
        else:
            print("Output and input don't match and are not possible for each other.")
            exit(1)
        


flag = True
#while(flag):
    #flag = runMain(test("newText.txt"))
flag = runMain(test("newText.txt"))