import math

def safe_log2(x: float) -> float:
    return math.log(x, 2) if x > 0 else 0.0

def entropy(rows, target):
    label_counts = {}
    for row in rows:
        y = row[target]
        label_counts[y] = label_counts.get(y, 0) + 1

    total = len(rows)
    H = 0.0
    for c in label_counts.values():
        p = c / total
        H += -p * safe_log2(p)
    return H, label_counts

def display_entropy_only(rows, target):
    n = len(rows)
    if n == 0:
        print("Dataset is empty.")
        return

    H_S, label_counts = entropy(rows, target)

    print("\n" + "="*60)
    print("INTERMEDIATE ENTROPY CALCULATION")
    print("="*60)
    print(f"Target Variable: {target}")
    print(f"Total examples (n): {n}")
    
    labels_sorted = sorted(label_counts.keys())
    print("\nStep 1: Class Counts")
    for L in labels_sorted:
        print(f" - {L}: {label_counts[L]}")

    print("\nStep 2: Probability and Log Calculation")
    parts = []
    for L in labels_sorted:
        c = label_counts[L]
        p = c / n
        log_val = safe_log2(p)
        term = -p * log_val
        parts.append(f"-({c}/{n})*log2({c}/{n})")
        print(f" - p({L}) = {c}/{n} = {p:.4f} | log2(p) = {log_val:.4f} | term = {term:.4f}")

    print("\nStep 3: Final Summation")
    formula = " + ".join(parts)
    print(f"H(S) = {formula}")
    print(f"RESULT: Entropy H(S) = {H_S:.4f}")
    print("="*60 + "\n")

def load_dataset_from_txt(filename):
    data = []
    with open(filename, "r") as f:
        lines = list(filter(None, f.read().splitlines()))

    headers = [h.strip() for h in lines[0].split(",")]
    for line in lines[1:]:
        values = [v.strip() for v in line.split(",")]
        if len(values) == len(headers):
            row = {headers[i]: values[i] for i in range(len(headers))}
            data.append(row)
    return data, headers[-1] # Returns data and the target column name

if __name__ == "__main__":
    filename = input("Enter dataset filename (e.g., data.txt): ").strip()
    try:
        data, target = load_dataset_from_txt(filename)
        display_entropy_only(data, target)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

