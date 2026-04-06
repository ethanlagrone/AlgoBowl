board_size = 97
grid = [['.' for _ in range(board_size)] for _ in range(board_size)]
steps_to_center = 0.25 * board_size + 0.75
stop = int(board_size / 2) - int(steps_to_center) + 1

for i in range(1, stop):
    grid[i][int(board_size / 2) - (i - 1)] = 'b'
    grid[i][int(board_size / 2) + (i - 1)] = 'b'

grid[int(board_size / 2)][int(board_size / 2)] = 'H'

with open("TeamInput.txt", "w") as f:
    for row in grid:
        f.write(''.join(row) + "\n")