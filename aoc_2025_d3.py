import unittest

# ---- Part 1 -----
# Given a line of numbers, you must find the largest possible
# two digit number that can be made.
# If given 12345, the largest number to be made would be 45.
# Or 4123912, the largest number would be 92.

# I think one way to solve this is iterating through the number digit by digit
# and figuring out which digit is the largest as well as the second largest.
# Keeping in mind what position they are in as well.

# Could also use a dictionary with the digit being the key and the values being
# a list of indexes that the number is found in.
# Then, give that we know the number and its indexes, we can figure out which number
# would be the largest number possible by figuring out the largest number at the smallest
# index.

# I attempted to use an enumerate function and storing digits: indexes into a dict.
# Which then I would try and form the largest number possible with two digits that have the smallest index.
# The largest tens digit would be an index that wasn't the last position for a bank.
# However, I quickly found I was vastly over complicating the problem.
# And ended up with too many nested loops that made me feel lost.


with open("aoc_d3_input.txt") as file:
	# Input is given with a single instruction per line.
	# Read the input file and place each line into a list.
	batteries = [line.rstrip("\n") for line in file]


# Return the highest joltage for a bank.
def get_joltage_for_bank(bank: str) -> int:
	# highest number can't be at the end.
	highest: int = max(bank[:-1])
	# second highest number would have to be any number after the index of the highest.
	second_highest: int = max(bank[bank.index(highest)+1:])
	joltage: str = f"{highest}{second_highest}"

	return int(joltage)

# ----- Part 2 -----
# I spent a long time and just went straight into part 2 without writing my thoughts.
# It was quite similar to the part 1, but instead we'd need to find 12 numbers instead of 2.
# We'd make a sliding window that decreases with each iteration. The largest number would have to be
# towards the start of the bank as it'd need to fit 11 more numbers after it.
# So find largest number that occurs first, then get rid of it, and slowly shrink the window on the left side.

def get_joltage_for_bank_twelve_batteries(bank: str) -> int:
	battery_str: str = ""
	cursor: int = 0
	# Create a sliding window that decrements each loop.
	# The window starts with the highest number found that has at least 11 more characters after it.
	# As there needs to be at least 12 batteries on.
	# The largest number is then added to a string that is tracking the largest number for each iteration.
	for idx in range(12, 0, -1):
		curr_range = bank[cursor:len(bank)-idx+1]
		curr_max = max(curr_range)
		battery_str += str(curr_max)
		cursor += curr_range.index(curr_max)+1

	return int(battery_str)




# adjusted to a passed parameter for part 2.
def get_total_joltage(batteries: list[str], get_joltage_for_bank) -> int:
	total_joltage = 0
	for bank in batteries:
		total_joltage += get_joltage_for_bank(str(bank))

	return total_joltage

print(get_total_joltage(batteries, get_joltage_for_bank))
print(get_total_joltage(batteries, get_joltage_for_bank_twelve_batteries))


class Test(unittest.TestCase):
	def test_part_one(self):
		batteries = [987654321111111, 811111111111119, 234234234234278, 818181911112111]
		self.assertEqual(get_total_joltage(batteries, get_joltage_for_bank), 357)

	def test_part_two(self):
		batteries = [987654321111111, 811111111111119, 234234234234278, 818181911112111]
		self.assertEqual(get_total_joltage(batteries, get_joltage_for_bank_twelve_batteries), 3121910778619)


if __name__ == "__main__":
	unittest.main()