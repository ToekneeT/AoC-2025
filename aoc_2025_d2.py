import unittest

# ---- Part 1 -----
# Given an input on a single line with each ID range separated by a comma.
# Find which IDs are not valid within the range.
# Invalid IDs are any that are repeated twice, such as 55 (5 twice), 6464 (64 twice), and 123123 (123 twice).
# Numbers can't have a leading 0. 0101 isn't valid, while 101 is valid.
# The answer is summing up all the invalid IDs.

# It seems that the repeating is really only happening when the amount of digits are even, as it makes an exact split.


with open("aoc_d2_input.txt") as file:
	# Input is given with a single line separated by a comma.
	line = file.read().strip()
	ids = [x for x in line.split(",")]


def find_invalid_ids(ids: list[str]) -> list[int]:
	invalid_ids: list[int] = []
	for id_range in ids:
		start, end = id_range.split("-")

		# Make the end inclusive as we want to check the last number as well.
		for id in range(int(start), int(end)+1):
			id_length = len(str(id))
			id_length_half = id_length // 2
			if id_length % 2 == 0 and str(id)[:id_length_half] == str(id)[id_length_half:]:
				invalid_ids.append(id)

	return invalid_ids


# ----- Part 2 -----
# IDs are now invalid if the sequence of digits repeats at least twice.
# 12341234 invalid (1234 two times).
# 123123123 (123 three times).
# 1212121212 (12 five times).

# This one is a bit more challenging to think about.
# First thought would be that we look at the first number and wait until it finds that number again in
# a sequence. From there we say a sequence is the first number up until it finds the same number again.
# So we have 143143. First number is 1, we check the next number which is 4, okay, 14, then the next number, 3, okay,
# 143, the next number is 1, which is the same as the starting number of 1, so we can say the sequence is 143.


def find_invalid_ids_2(ids: list[str]) -> list[int]:
	invalid_ids: list[int] = []
	for id_range in ids:
		start, end = id_range.split("-")

		for id in range(int(start), int(end)+1):
			id_length = len(str(id))
			id_length_half = id_length // 2
			if id_length % 2 == 0 and str(id)[:id_length_half] == str(id)[id_length_half:]:
				invalid_ids.append(id)
				# Skip past the rest of the loops if the number is invalid as there's no need to check further.
				continue

			
			# Create a set of unique repeating sequences.
			seen = set()
			id_num = str(id)
			# Only really need to check half of the input as we know it's not repeating due to the outer loop.
			for seq_length in range(1, len(id_num)//2 + 1):
				left_cursor = 0
				# Clears the set for a new group of seen numbers.
				seen.clear()

				while left_cursor < len(id_num):
					right_cursor = left_cursor + seq_length

					# Adds a substring or sequence into a set.
					# If the sequence already exists in the set, it'll stay at a length of 1.
					# However, if the set ever has more than 1, then we know that there's a non duplicate sequence.
					seen.add(id_num[left_cursor:right_cursor])
					if len(seen) > 1:
						break
					left_cursor += seq_length

				# If the set only has 1 sequence, then that means the entire string is repeating.
				if len(seen) == 1:
					invalid_ids.append(id)

	return invalid_ids


# print(sum(find_invalid_ids(ids)))
# print(sum(find_invalid_ids_2(ids)))

class Test(unittest.TestCase):
	# Funny story about this case.
	# I ran the find_invalid_ids function on my input before I ran this test case.
	# I put my answer into AoC, and it was accepted.
	# Running this test case, I found that it kept failing, number was off.
	# Odd, so I made sure the example input was the same.
	# Turns out, the for loop in the function was exclusive, so it wasn't counting the 22 from the first input.
	# And my puzzle input just didn't have such scenario.
	def test_example_case(self):
		ids = ["11-22", "95-115", "998-1012", "1188511880-1188511890", "222220-222224", "1698522-1698528",\
		"446443-446449", "38593856-38593862", "565653-565659", "824824821-824824827", "2121212118-2121212124"]
		self.assertEqual(sum(find_invalid_ids(ids)), 1_227_775_554)


	def test_example_cast_two(self):
		ids = ["11-22", "95-115", "998-1012", "1188511880-1188511890", "222220-222224", "1698522-1698528",\
		"446443-446449", "38593856-38593862", "565653-565659", "824824821-824824827", "2121212118-2121212124"]
		self.assertEqual(sum(find_invalid_ids_2(ids)), 4_174_379_265)




if __name__ == "__main__":
	unittest.main()