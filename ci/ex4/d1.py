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
    probs = []
    for c in label_counts.values():
        p = c / total
        probs.append(p)
        H += -p * safe_log2(p)
    return H, label_counts, probs

def unique_values(rows, attr):
    seen = set()
    vals = []
    for row in rows:
        v = row[attr]
        if v not in seen:
            seen.add(v)
            vals.append(v)
    return vals

def split_by_value(rows, attr):
    groups = {}
    for row in rows:
        v = row[attr]
        groups.setdefault(v, []).append(row)
    return groups

def step_by_step_report(rows, attributes, target):
    n = len(rows)
    H_S, label_counts, _ = entropy(rows, target)

    print("\n" + "="*60)
    print("INTERMEDIATE CALCULATION REPORT")
    print("="*60)
    print(f"Total examples: {n}")
    
    labels_sorted = sorted(label_counts.keys())
    parts = []
    for L in labels_sorted:
        c = label_counts.get(L, 0)
        p = c / n
        parts.append(f"-({c}/{n})*log2({c}/{n})")
    
    print(f"Entropy H(S) = {' + '.join(parts)} = {H_S:.4f}")
    print(f"Class counts: {', '.join([f'{L}={label_counts[L]}' for L in labels_sorted])}")
    print("-" * 30)

    ig_results = []

    for attr in attributes:
        print(f"\nEvaluating Attribute: {attr}")
        groups = split_by_value(rows, attr)
        weighted_terms = []
        H_after = 0.0
        
        for v in unique_values(rows, attr):
            subset = groups[v]
            n_v = len(subset)
            H_v, counts_v, _ = entropy(subset, target)
            weight = n_v / n
            H_after += weight * H_v

            # Detailed subset entropy expression
            parts_v = []
            for L in labels_sorted:
                c = counts_v.get(L, 0)
                if c > 0:
                    parts_v.append(f"-({c}/{n_v})*log2({c}/{n_v})")
            
            print(f"  Value '{v}': |S_v|={n_v} | Counts: {', '.join([f'{L}={counts_v.get(L,0)}' for L in labels_sorted])}")
            if parts_v:
                print(f"    H(S_{v}) = {' + '.join(parts_v)} = {H_v:.4f}")
            else:
                print(f"    H(S_{v}) = 0.0000")
            
            weighted_terms.append(f"({n_v}/{n})*{H_v:.4f}")

        print(f"  Sum of weighted entropies H(S|{attr}) = {' + '.join(weighted_terms)} = {H_after:.4f}")
        IG = H_S - H_after
        print(f"  RESULT: Information Gain IG(S, {attr}) = {H_S:.4f} - {H_after:.4f} = {IG:.4f}")
        ig_results.append((attr, IG))

    print("\n" + "="*40)
    print("FINAL SUMMARY OF INFORMATION GAIN")
    print("="*40)
    for attr, IG in ig_results:
        print(f"- {attr:15s} -> IG = {IG:.4f}")

    best_attr, best_IG = max(ig_results, key=lambda x: x[1])
    print(f"\nROOT NODE SELECTED: {best_attr}")
    print(f"Highest Information Gain: {best_IG:.4f}")
    print("="*40 + "\n")

def loads_dataset_from_txt(filename):
    data = []
    with open(filename, "r") as f:
        # filter(None, ...) handles the empty trailing lines on Linux
        lines = list(filter(None, f.read().splitlines()))

    headers = lines[0].split(",")
    for line in lines[1:]:
        line = line.strip()
        if not line: continue
        values = line.split(",")
        if len(values) == len(headers):
            row = {headers[i]: values[i] for i in range(len(headers))}
            data.append(row)
    return data, headers[:-1], headers[-1]

if __name__ == "__main__":
    filename = input("Enter dataset filename (e.g., data.txt): ").strip()
    try:
        data, attributes, target = loads_dataset_from_txt(filename)
        if not data:
            print("Error: No data found in file.")
        else:
            step_by_step_report(data, attributes, target)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
