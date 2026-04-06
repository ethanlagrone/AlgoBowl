board_size = 97
center = int(board_size / 2)
grid = [['.' for _ in range(board_size)] for _ in range(board_size)]

steps_to_center = 0.25 * board_size + 0.75
stop_top = center - int(steps_to_center) + 1

side_row_count = 2 * (stop_top - 1) - 1
start_sides = stop_top + 2
end_sides = start_sides + side_row_count

start_bottom = center + int(steps_to_center)


for i in range(1, stop_top):
    grid[i][center - (i - 1)] = 'b'
    grid[i][center + (i - 1)] = 'b'

for i in range(start_sides, center):
    grid[i][center - i + 1] = 'b'
    grid[i][board_size - 1 - (i - 2 * (i - start_sides)) - 1 + 4] = 'b'     # yeah idk either

grid[center][1] = 'b'
grid[center][board_size - 2] = 'b'
grid[center][center] = 'H'

with open("TeamInput.txt", "w") as f:
    for row in grid:
        f.write(''.join(row) + "\n")