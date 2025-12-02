import unittest

# ---- Part 1 -----
# The problem gives instructions line by line.
# Either a L or R for which way the number goes.
# Initially it starts at 50.
# The number after the letter indicates how many numbers it goes in a direction.
# Numbers go from 0-99, it'll reset, or going past 99 will end in 0, going under 0 results in 99.
# The problem wants to know how many times the rotations end up pointing at 0.
# A simple way to solve this is using modulous. Any L is a negative input, while a R is a positive input.


with open("aoc_d1_input.txt") as file:
	# Input is given with a single instruction per line.
	# Read the input file and place each line into a list.
	instructions = [line.rstrip("\n") for line in file]


def rotate_lock(instructions: list[str]) -> int:
	dial_pos: int = 50
	pos_zero_hits: int = 0
	for instruc in instructions:
		rotation_amount = int(instruc[1:])
		if instruc[0] == "L":
			dial_pos = (dial_pos - rotation_amount) % 100
		else:
			dial_pos = (dial_pos + rotation_amount) % 100

		if dial_pos == 0:
			pos_zero_hits += 1

	return pos_zero_hits


# ----- Part 2 -----
# Similar to part 1, but instead it's now whenever the number would *pass* zero instead of landing directly on it.
# Another simple solution. Before performing modulous, check to see if the number is above or below 100.
# ------------------------------
# I was getting an answer that was too low, which led me to look through the input for a specific case.
# To my dismay, that case was true, rotations can be more than 100 at a time. (instructions mention that, which I skimmed past.)

def rotate_lock_2(instructions: list[str]) -> int:
	dial_pos: int = 50
	pos_zero_clicks: int = 0
	for instruc in instructions:
		rotation_amount = int(instruc[1:])
		# If the rotation amount is larger than 100, we know it'll make 1 full rotation.
		if rotation_amount >= 100:
			# Given that a 100 is a full rotation, we can just add a single full rotation
			# to the times it passes zero.
			# We then only need to worry about anything under 100 again, so we modulous again.
			pos_zero_clicks += rotation_amount // 100
			rotation_amount %= 100

		if instruc[0] == "L":
			if dial_pos > 0 and dial_pos - rotation_amount <= 0:
				pos_zero_clicks += 1
			dial_pos = (dial_pos - rotation_amount) % 100
		else:
			if dial_pos < 100 and dial_pos + rotation_amount >= 100:
				pos_zero_clicks += 1
			dial_pos = (dial_pos + rotation_amount) % 100

	return pos_zero_clicks


class Test(unittest.TestCase):
	def test_part_one(self):
		instructions = ["L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"]
		self.assertEqual(rotate_lock(instructions), 3)

	def test_part_two(self):
		instructions = ["L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"]
		self.assertEqual(rotate_lock_2(instructions), 6)

	def test_part_two_large_rotations(self):
		instructions = ["L68", "R133"]
		self.assertEqual(rotate_lock_2(instructions), 3)

	def test_part_two_thousand_rotation(self):
		instructions = ["R1000"]
		self.assertEqual(rotate_lock_2(instructions), 10)


if __name__ == "__main__":
	unittest.main()