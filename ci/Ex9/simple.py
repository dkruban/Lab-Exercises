# Simple probability calculations for coin toss and dice roll

def coin_probability():
	outcomes = ['Heads', 'Tails']
	probability = 1 / len(outcomes)
	print("Coin Toss Probabilities:")
	for outcome in outcomes:
		print(f"P({outcome}) = {probability}")

def dice_probability():
	sides = 6
	probability = 1 / sides
	print("\nDice Roll Probabilities:")
	for i in range(1, sides + 1):
		print(f"P({i}) = {probability}")

if __name__ == "__main__":
	coin_probability()
	dice_probability()
