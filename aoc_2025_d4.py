import unittest, copy

# ----- Part 1 -----
# The problem needs to find out how many rolls of paper, @, can be harvested.
# A roll of paper can only be harvested as long as there are less than 4 rolls
# adjacent to it.

# This can be done with a nested loop.
# One that checks the Y, the other that checks X.
# It'd check x-1, x+1, y+1, y-1, x-1 & y-1, x+1 & y+1, x-1 & y+1, x+1 & y-1.
# If at any point, there are more than 3 rolls, it can then continue on to the next spot.

# One loop that checks the X, the other loop checks the Y, which is taken from a 
# different grid that grabs the columns.
# Or, we can get a subgrid of each section with it being a 3x3, we can check to see
# how many rolls exists in it, and determine if it's possible or not.

with open("aoc_d4_input.txt") as file:
	# Input is given with a single instruction per line.
	# Read the input file and place each line into a list.
	diagram = [line.rstrip("\n") for line in file]


# Puts all the columns of the grid into a list and returns it.
def transpose_grid(board):
    cols = []
    for i in range(len(board)):
        col = []
        for j in range(len(board)):
            col.append(board[j][i])
        cols.append(col)
    return cols


# Let's say we get a sub grid, 3x3 for each section.
# We can then check if the center has a roll in it, and if it does,
# we can determine how many rolls exist in the subgrid, which will determine if
# that specific roll is valid or not.

# On second hand, thinking about it more, this doesn't seem to work as well as I'd hope.
# This really only checks the the center piece, which would still find a lot.
# However, this wouldn't work for the edges of the grid.
# For example:
# ..@@@..
# .@@@@..
# Index [3, 0] wouldn't be valid, but the subgrid wouldn't
# be checking that one, it'd only be checking [1, 1]
# def get_subgrid(board):
#     subgrid = []
#     # The iterable jumps by the subgrid size each loop.
#     for col in range(0, len(board), 3):
#         for row in range(0, len(board), 3):
#             grid = []
#             for i in range(3):
#                 for j in range(3):
#                     # (row, col) defines the top-left corner of the subgrid, and 
#                     # (i, j) is a local coordinate offset within the subgrid, scanning
#                     # through each cell, row-by-row. This definition means that (row i, col + j)
#                     # is effecitevly a translation from a local to a global coordinate on the 
#                     # entire grid that defines the position of the subgrid cell.
#                     grid.append(board[col + i][row + j])
#             subgrid.append(grid)
#     return subgrid


# def is_valid_roll(subgrid):
# 	# 4

# I may be overthinking it again.
# Can probably just have a nested for loop, which will give me both an X and Y coordinate.
# From there, it's just the +1-1 thing from above to check if that index contains an @.
# Which is a brute force way of doing it.

# print(diagram[0])
# print()
# print(transpose_grid(diagram)[0])

def count_surrounding_rolls(diagram: list[str], y0: int, x0: int) -> int:
	# Prevent it from going out of bounds, in other words the edges of the diagram.
	x1 = x0-1 if x0-1 > 0 else 0
	x2 = x0+1 if x0+1 < len(diagram[0])-1 else len(diagram[0])-1
	y1 = y0-1 if y0-1 > 0 else 0
	y2 = y0+1 if y0+1 < len(diagram)-1 else len(diagram)-1
	# If I want to get all 8 surrounding squares, I'd need
	# [x0, y0], [x1, y0], [x2, y0], [x0, y1], [x1, y1], [x2, y1], [x0, y2], [x1, y2], [x2, y2]

	# This might be a litte hacky.
	# Lists can't be added into a set as far as I'm aware.
	# So instead, I added the x and y coordinate as number,number.
	# Then split by the comma later to use as the indices.
	coords = set()
	for x in [x0, x1, x2]:
		for y in [y0, y1, y2]:
			if x == x0 and y == y0:
				continue
			coords.add(f'{x},{y}')

	rolls: list[str] = []
	for coord in coords:
		x, y = coord.split(",")
		rolls.append(diagram[int(x)][int(y)])

	return rolls.count("@")

# print(count_surrounding_rolls(diagram, 0, 1))


def part_one(diagram: list[str]) -> int:
	valid_roll: int = 0
	for row in range(len(diagram)):
		for col in range(len(diagram[row])):
			if count_surrounding_rolls(diagram, row, col) < 4 and diagram[col][row] == "@":
				valid_roll += 1

	return valid_roll

print(part_one(diagram))


# ----- Part 2 -----
# Part 2 is retroactively removing the rolls if they're possible to remove.
# This is partly what I was thinking of originally when thinking of the problem.
# I think what could be done is reconstructing the string, replacing the @ with a .

# I misunderstood. I thought it was retroactively removing the rolls as it was going through.
# But in actuality, it's running through it entirely, and then removing the rolls, then running again.


def reconstruct_string(diagram: list[str], x: int, y: int) -> None:
	diagram[x] = diagram[x][:y] + "." + diagram[x][y+1:]


def part_two(diagram: list[str]) -> int:
	valid_roll: int = 0

	while True:
		valid_roll_index: list[[int, int]] = []
		for row in range(len(diagram)):
			for col in range(len(diagram[row])):
				if count_surrounding_rolls(diagram, row, col) < 4 and diagram[col][row] == "@":
					valid_roll += 1
					valid_roll_index.append([row, col])

		# If there were no rolls removed, then we can exit the loop as
		# running through the loop would result in the same thing.
		if not valid_roll_index:
			break

		for x, y in valid_roll_index:
			reconstruct_string(diagram, y, x)

	return valid_roll


print(part_two(diagram))


class Test(unittest.TestCase):
	def test_part_one(self):
		diagram = [
		"..@@.@@@@.",
		"@@@.@.@.@@",
		"@@@@@.@.@@",
		"@.@@@@..@.",
		"@@.@@@@.@@",
		".@@@@@@@.@",
		".@.@.@.@@@",
		"@.@@@.@@@@",
		".@@@@@@@@.",
		"@.@.@@@.@."
		]
		self.assertEqual(part_one(diagram), 13)

	def test_part_two(self):
		diagram = [
		"..@@.@@@@.",
		"@@@.@.@.@@",
		"@@@@@.@.@@",
		"@.@@@@..@.",
		"@@.@@@@.@@",
		".@@@@@@@.@",
		".@.@.@.@@@",
		"@.@@@.@@@@",
		".@@@@@@@@.",
		"@.@.@@@.@."
		]
		self.assertEqual(part_two(diagram), 43)


if __name__ == "__main__":
	unittest.main()