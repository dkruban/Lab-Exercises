# Full joint probability distribution for Toothache, Cavity, and Catch

# Example probabilities (from AIMA or similar sources)
# P(Toothache, Cavity, Catch)

def get_user_distribution():
	print("Enter the full joint probability distribution for Toothache, Cavity, and Catch.")
	print("For each combination, enter the probability (sum must be 1.0). Leave blank to use default values.")
	keys = [
		(True, True, True), (True, True, False),
		(True, False, True), (True, False, False),
		(False, True, True), (False, True, False),
		(False, False, True), (False, False, False)
	]
	default = [0.108, 0.012, 0.016, 0.064, 0.072, 0.008, 0.144, 0.576]
	joint_distribution = {}
	for i, k in enumerate(keys):
		prompt = f"P(Toothache={k[0]}, Cavity={k[1]}, Catch={k[2]}): "
		val = input(prompt)
		if val.strip() == '':
			prob = default[i]
		else:
			try:
				prob = float(val)
			except ValueError:
				print("Invalid input, using default value.")
				prob = default[i]
		joint_distribution[k] = prob
	total = sum(joint_distribution.values())
	if abs(total - 1.0) > 1e-6:
		print(f"Warning: Probabilities sum to {total}, not 1.0. Normalizing.")
		for k in joint_distribution:
			joint_distribution[k] /= total
	return joint_distribution

def print_joint_distribution(joint_distribution):
	print("Full Joint Probability Distribution (Toothache, Cavity, Catch):")
	print("Toothache\tCavity\tCatch\tProbability")
	for (toothache, cavity, catch), prob in joint_distribution.items():
		print(f"{toothache}\t{cavity}\t{catch}\t{prob}")

def get_inference_query():
	print("\nEnter your inference query in the form:")
	print("Variable=value (comma separated for multiple conditions). Example: Cavity=True,Toothache=False")
	query = input("Query (leave blank for none): ")
	if not query.strip():
		return {}, {}
	conditions = query.split(",")
	evidence = {}
	for cond in conditions:
		if '=' in cond:
			var, val = cond.split('=')
			var = var.strip().capitalize()
			val = val.strip().lower() == 'true'
			evidence[var] = val
	return evidence, {}

def infer(joint_distribution, evidence, query_vars=None):
	# If query_vars is empty, just return the probability of the evidence
	if not evidence:
		return None
	num = 0.0
	denom = 0.0
	for k, prob in joint_distribution.items():
		assign = {'Toothache': k[0], 'Cavity': k[1], 'Catch': k[2]}
		match_evidence = all(assign.get(var) == val for var, val in evidence.items())
		if match_evidence:
			num += prob
		denom += prob
	if denom == 0:
		return 0.0
	return num / denom


if __name__ == "__main__":
	joint_distribution = get_user_distribution()
	print_joint_distribution(joint_distribution)
	while True:
		evidence, query_vars = get_inference_query()
		if evidence:
			prob = infer(joint_distribution, evidence, query_vars)
			print(f"\nP({evidence}) = {prob}")
		else:
			print("No inference query provided.")
