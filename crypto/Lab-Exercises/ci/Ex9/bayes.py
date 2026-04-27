# Bayes' Rule demonstration: P(Cavity | Toothache)

# Example joint probabilities (same as in fulljoin.py)

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


def get_bayes_query():
	print("\nEnter your Bayes' rule query in the form:")
	print("QueryVar=Value | EvidenceVar=Value (comma separated for multiple evidence). Example: Cavity=True | Toothache=True")
	query = input("Query (leave blank for P(Cavity|Toothache=True)): ")
	if not query.strip():
		return {'Cavity': True}, {'Toothache': True}
	if '|' not in query:
		print("Invalid format. Using default: P(Cavity|Toothache=True)")
		return {'Cavity': True}, {'Toothache': True}
	left, right = query.split('|')
	left = left.strip()
	right = right.strip()
	query_vars = {}
	evidence = {}
	for cond in left.split(','):
		if '=' in cond:
			var, val = cond.split('=')
			query_vars[var.strip().capitalize()] = val.strip().lower() == 'true'
	for cond in right.split(','):
		if '=' in cond:
			var, val = cond.split('=')
			evidence[var.strip().capitalize()] = val.strip().lower() == 'true'
	return query_vars, evidence

def bayes_rule(joint_distribution, query_vars, evidence):
	# Compute P(QueryVars | Evidence) = P(QueryVars and Evidence) / P(Evidence)
	def match(assign, cond):
		return all(assign.get(var) == val for var, val in cond.items())
	num = 0.0
	denom = 0.0
	for k, prob in joint_distribution.items():
		assign = {'Toothache': k[0], 'Cavity': k[1], 'Catch': k[2]}
		if match(assign, evidence):
			denom += prob
			if match(assign, query_vars):
				num += prob
	if denom == 0:
		print("P(Evidence) is zero, cannot compute Bayes' rule.")
		return None
	return num / denom


if __name__ == "__main__":
	joint_distribution = get_user_distribution()
	while True:
		query_vars, evidence = get_bayes_query()
		prob = bayes_rule(joint_distribution, query_vars, evidence)
		if prob is not None:
			print(f"\nP({query_vars} | {evidence}) = {prob}")
