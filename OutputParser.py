#Needs to return the maze and score

def takeOutput():
    score = int(input())
    maze = []

    while(True):
        line = list(input())
        if not line:
            break
        maze.append(line)

    return maze, score
