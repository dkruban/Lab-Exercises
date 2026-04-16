import math

def safe_log2(x: float) -> float:
    """Calculates log2, returning 0 if input is 0 to avoid errors."""
    return math.log(x, 2) if x > 0 else 0.0

def display_entropy_steps(rows, target):
    n = len(rows)
    if n == 0:
        print("Dataset is empty.")
        return

    # 1. Count occurrences
    label_counts = {}
    for row in rows:
        y = row[target]
        label_counts[y] = label_counts.get(y, 0) + 1

    print("\n" + "="*65)
    print("      STEP-BY-STEP ENTROPY CALCULATION (H(S))")
    print("="*65)
    print(f"Target Column: {target}")
    print(f"Total Samples (n): {n}")

    # 2. Show Counts
    print("\n[STEP 1] Class Counts:")
    labels_sorted = sorted(label_counts.keys(), reverse=True) # Sort 'yes' then 'no'
    for L in labels_sorted:
        print(f" - Count({L}) = {label_counts[L]}")

    # 3. Probability & Log terms
    print("\n[STEP 2] Calculate Probabilities (p_i) and Log Terms:")
    total_entropy = 0.0
    formula_parts = []
    
    for L in labels_sorted:
        count = label_counts[L]
        p = count / n
        log_val = safe_log2(p)
        term = -p * log_val
        total_entropy += term
        
        formula_parts.append(f"-({count}/{n} * log2({count}/{n}))")
        
        print(f" - For '{L}':")
        print(f"    p = {count}/{n} = {p:.4f}")
        print(f"    log2({p:.4f}) = {log_val:.4f}")
        print(f"    Term [-p * log2(p)] = -({p:.4f} * {log_val:.4f}) = {term:.4f}")

    # 4. Final Result
    print("\n[STEP 3] Final Summation:")
    print(f" H(S) = {' + '.join(formula_parts)}")
    print(f" H(S) = {total_entropy:.4f}")
    print("="*65)

def load_data():
    """Manual load for the 4 Yes / 3 No dataset provided."""
    headers = ["age", "income", "student", "credit_rating", "buys_computer"]
    raw_rows = [
        ["middle_aged", "medium", "yes", "fair", "yes"],
        ["middle_aged", "low", "yes", "excellent", "yes"],
        ["middle_aged", "low", "yes", "excellent", "yes"],
        ["middle_aged", "high", "no", "excellent", "yes"],
        ["youth", "medium", "no", "excellent", "no"],
        ["senior", "medium", "yes", "excellent", "no"],
        ["senior", "medium", "no", "excellent", "no"]
    ]
    # Convert to list of dictionaries
    data = [dict(zip(headers, row)) for row in raw_rows]
    return data, headers[-1]

if __name__ == "__main__":
    # You can use the load_dataset_from_txt function from previous steps,
    # but here we use the specific 4 Yes / 3 No data directly for clarity.
    data, target_col = load_data()
    display_entropy_steps(data, target_col)

