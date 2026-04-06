# this code is some BULLSHIT
# if we decide we want to slightly change how the input works, morgan is capable of updating this code

board_size = 97
center = int(board_size / 2)
grid = [['.' for _ in range(board_size)] for _ in range(board_size)]

steps_to_center = 0.25 * board_size + 0.75
stop_top = center - int(steps_to_center) + 1

side_row_count = 2 * (stop_top - 1) - 1
start_sides = stop_top + 2
stop_sides = start_sides + side_row_count

start_bottom = center + int(steps_to_center)

# insert top bees
for i in range(1, stop_top):
    grid[i][center - (i - 1)] = 'b'
    grid[i][center + (i - 1)] = 'b'

# insert first half of side bees
for i in range(start_sides, center):
    grid[i][center - i + 1] = 'b'
    grid[i][i - center - 2] = 'b'

# insert center bees + horse
grid[center][1] = 'b'
grid[center][board_size - 2] = 'b'
grid[center][center] = 'H'

# insert second half of side bees
for i in range(center + 1, stop_sides):
    grid[i][i - center + 1] = 'b'
    grid[i][center - i - 2] = 'b'

# insert bottom bees
for i in range(start_bottom, board_size - 1):
    grid[i][i - center + 1] = 'b'
    grid[i][center - 2 - i] = 'b'

with open("TeamInput.txt", "w") as f:
    for row in grid:
        f.write(''.join(row) + "\n")