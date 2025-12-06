import unittest

# ---- Part 1 -----



with open("aoc_d5_input.txt") as file:
	# Input is given with a single instruction per line.
	# Read the input file and place each line into a list.
	puzz_input: str = [line.rstrip("\n") for line in file]


# The idea of this one is to get a set of available fresh ingredients.
# However, there's a large data set, which means that storing it all into
# a set would require too much memory, leading to a memory error.
# def parse_input(puzz_input: list[str]):
# 	fresh_ingredients = set()
# 	available_ingredients = []
# 	for line in puzz_input:
# 		ingredient_range = line.split("-")
# 		if len(ingredient_range) > 1:
# 			start, stop = ingredient_range[0], ingredient_range[1]
# 			for id in range(int(start), int(stop)+1):
# 				fresh_ingredients.add(id)
# 		if len(line.split("-")) == 1 and line != "":
# 			available_ingredients.append(int(line))

# 	return fresh_ingredients, available_ingredients


# def get_fresh_ingredients(fresh_ingredients, available_ingredients):
# 	fresh = 0
# 	for id in available_ingredients:
# 		if id in fresh_ingredients:
# 			fresh += 1

# 	return fresh


# The issue with this version is that it doesn't take care of duplicate ids.
# def get_fresh_ingredients(puzz_input: list[str], available_ingredients: list[int]) -> int:
# 	fresh_ingredients: int = 0
# 	possible_fresh_ingredients = set()
# 	for line in puzz_input:
# 		ingredient_range = line.split("-")
# 		if len(ingredient_range) > 1:
# 			start, stop = ingredient_range[0], ingredient_range[1]
# 			# This will have an issue as it'll increment the fresh ingredients 
# 			# even if it has seen the number before
# 			# as the range can overlap.
# 			for id in range(int(start), int(stop)+1):
# 				# print(id)
# 				possible_fresh_ingredients.add(id)
# 				if id in available_ingredients:
# 					fresh_ingredients += 1

# 	return fresh_ingredients


def get_available_ingredients(puzz_input):
	available_ingredients = []
	for line in puzz_input:
		ingredient_range = line.split("-")
		if len(ingredient_range) == 1 and line != "":
			available_ingredients.append(int(line))

	return available_ingredients

# # This way doesn't store the ranges in anything
# # However, it also doesn't take care of duplicates.
# # A way I was thinking of this was to take the ranges and put just the start and 
# # stop ranges into a list. Then we could figure out if the range is within another range
# # from before, and if it is, it can be skipped.
# def get_fresh_ingredients(puzz_input, available_ingredients):
# 	fresh_ingredients = 0
# 	for line in puzz_input:
# 		ingredient_range = line.split("-")
# 		if len(ingredient_range) > 1:
# 			start, stop = ingredient_range[0], ingredient_range[1]
# 			for id in available_ingredients:
# 				if id >= int(start) and id <= int(stop):
# 					fresh_ingredients += 1

# 	return fresh_ingredients


def get_fresh_ingredients(puzz_input):
	fresh_ingredients = []
	for line in puzz_input:
		ingredient_range = line.split("-")
		if len(ingredient_range) > 1:
			start, stop = ingredient_range[0], ingredient_range[1]
			fresh_ingredients.append((int(start), int(stop)))

	return fresh_ingredients


# Take the ranges and merge them into as few ranges as possible.
def merge_ranges(ranges):
	# Sort ranges by their start.
	ranges.sort(key=lambda x: x[0])
	merged_ranges = []

	current_start, current_end = ranges[0]

	for start, end in ranges[1:]:
		# if the start is within the range of the other end, then we
		# can set the end to the longer one.
		if start <= current_end + 1:
			current_end = max(current_end, end)
		else:
			# Set the range if it doesn't fit within the range.
			merged_ranges.append((current_start, current_end))
			current_start, current_end = start, end

	merged_ranges.append((current_start, current_end))

	return merged_ranges


# def get_valid_ingredients(merged_ranges, available_ingredients):
# 	fresh_ingredients = 0
# 	for start, stop in merged_ranges:
# 		for id in range(start, stop+1):
# 			if id in available_ingredients:
# 				fresh_ingredients += 1

# 	return fresh_ingredients

# import bisect
# # Binary search way of finding if the ingredients exist within the range.
# # This is fast and more efficient, however, it wasn't my idea originally.
# def get_valid_ingredients(merged_ranges, available_ingredients):
# 	fresh_ingredients = 0
# 	available_ingredients = sorted(available_ingredients)
# 	for start, stop in merged_ranges:
# 		left = bisect.bisect_left(available_ingredients, start)
# 		right = bisect.bisect_right(available_ingredients, stop)
# 		fresh_ingredients += (right - left)

# 	return fresh_ingredients


# Checks each ID in available ingredients and checks if it falls within
# the range of the merged range.
def get_valid_ingredients(merged_ranges, available_ingredients):
	fresh_ingredients = 0
	for id in available_ingredients:
		for start, stop in merged_ranges:
			if id >= start and id <= stop:
				fresh_ingredients += 1
				continue

	return fresh_ingredients


import time
start_time = time.time()
merged_ranges = merge_ranges(get_fresh_ingredients(puzz_input))
available_ingredients = get_available_ingredients(puzz_input)


print(get_valid_ingredients(merged_ranges, available_ingredients))
end_time = time.time()
print(f"Runtime: {end_time - start_time} seconds.")


# ----- Part 2 -----
# Now it just wants to know how many ingredients could be available.
# Basically go through the merged lists and subtract the start and stop of them.

def get_possible_valid_ingredients(merged_ranges):
	possible_valid = 0
	for start, stop in merged_ranges:
		possible_valid += (stop+1) - start

	return possible_valid


print(get_possible_valid_ingredients(merged_ranges))

class Test(unittest.TestCase):
	def test_part_one(self):
		with open("aoc_d5_ex_input.txt") as file:
			puzz_input: str = [line.rstrip("\n") for line in file]
		merged_ranges = merge_ranges(get_fresh_ingredients(puzz_input))
		available_ingredients = get_available_ingredients(puzz_input)
		self.assertEqual(get_valid_ingredients(merged_ranges, available_ingredients), 3)

	def test_part_two(self):
		with open("aoc_d5_ex_input.txt") as file:
			puzz_input: str = [line.rstrip("\n") for line in file]
		merged_ranges = merge_ranges(get_fresh_ingredients(puzz_input))
		self.assertEqual(get_possible_valid_ingredients(merged_ranges), 14)


if __name__ == "__main__":
	unittest.main()