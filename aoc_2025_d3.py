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