board_size = 97
grid = [['.' for _ in range(board_size)] for _ in range(board_size)]

for i in range(1, board_size - 1):
    grid[i][(board_size / 2) - (i - 1)] = 'b'
    grid[i][(board_size / 2) + (i - 1)] = 'b'

grid[board_size / 2][board_size / 2] = 'H'

with open("TeamInput.txt", "w") as f:
    for row in grid:
        f.write(''.join(row) + "\n")