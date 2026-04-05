#Needs to return the maze and score
import InputParser
import Helper

def outputParser(mazeIn, mazeOut):
    mazeTiles = {'.','H','#','W','a','b','c','p'}
    changable = ['.', 'W']
    inChangables = []
    outChangables = []

    mazeInRows = len(mazeIn)
    mazeOutRows = len(mazeOut)
    mazeInCols = len(mazeIn[0])
    mazeOutCols = len(mazeOut[0])

    if((mazeInRows != mazeOutRows) or (mazeInCols != mazeOutCols)):
       return False
    

    for i in range(len(mazeIn)):
      for j in range(len(mazeIn[i])):
         current = mazeIn[i][j]
         if(current in changable):
            inChangables.append((current,i,j))



    for i in range(len(mazeOut)):
      for j in range(len(mazeOut[i])):
         current = mazeIn[i][j]
         if(current not in mazeTiles):
            print("Unforseen tile in output")
            return False
         if(current in changable):
            outChangables.append((current,i,j))

    for element,i,j in inChangables:
       if((element,i,j) in outChangables):
          continue
       else:
          element = 'W'
          if((element,i,j) in outChangables):
             continue
          else:
             print("Something was changed that shouldn't have been")
             return False
          
    return True