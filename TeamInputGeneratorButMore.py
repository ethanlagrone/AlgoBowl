# this is an updated version of the generator that puts more bees on the map

n = 49
board_size = 2 * n - 1
wall_count = 4 * n - 4

center = int(board_size / 2)
grid = [['.' for _ in range(board_size)] for _ in range(board_size)]

steps_to_center = int(0.25 * board_size + 0.75)
triangle_height = steps_to_center - 2

# top bees
for i in range(1, triangle_height + 1):
    row = i
    width = i - 1
    start_j = center - width
    end_j = center + width
    for j in range(start_j, end_j + 1, 2):
        grid[row][j] = 'b'
        if i == triangle_height:
            if j == start_j: # First gap
                grid[row][j + 1] = 'a'
            elif j == end_j - 2: # Last gap (before the final 'b')
                grid[row][j + 1] = 'a'

# bottom bees
for i in range(1, triangle_height + 1):
    row = (board_size - 1) - i
    width = i - 1
    start_j = center - width
    end_j = center + width
    for j in range(start_j, end_j + 1, 2):
        grid[row][j] = 'b'
        if i == triangle_height:
            if j == start_j:
                grid[row][j + 1] = 'a'
            elif j == end_j - 2:
                grid[row][j + 1] = 'a'

# left bees
for j in range(1, triangle_height + 1):
    col = j
    width = j - 1
    start_i = center - width
    end_i = center + width
    for i in range(start_i, end_i + 1, 2):
        grid[i][col] = 'b'
        if j == triangle_height:
            if i == start_i:
                grid[i + 1][col] = 'a'
            elif i == end_i - 2:
                grid[i + 1][col] = 'a'

# right bees
for j in range(1, triangle_height + 1):
    col = (board_size - 1) - j
    width = j - 1
    start_i = center - width
    end_i = center + width
    for i in range(start_i, end_i + 1, 2):
        grid[i][col] = 'b'
        if j == triangle_height:
            if i == start_i:
                grid[i + 1][col] = 'a'
            elif i == end_i - 2:
                grid[i + 1][col] = 'a'

# horse and trivial walls
grid[center][center] = 'H'

grid[center - 1][center] = 'W'
grid[center][center - 1] = 'W'
grid[center][center + 1] = 'W'
grid[center + 1][center] = 'W'

with open("TeamInput.txt", "w") as f:
    f.write(f'{wall_count}\n')
    f.write(f'{board_size} {board_size}\n')
    for row in grid:
        f.write(''.join(row) + "\n")
    f.write("0")