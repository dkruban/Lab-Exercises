import math
import csv
import random

def load_data(filename):
    X, y = [], []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader) # Skip header
            for row in reader:
                if not row: continue
                X.append([float(x) for x in row[:-1]])
                y.append(row[-1].strip())
    except Exception as e:
        print(f"File Error: {e}")
    return X, y

def get_stats(data):
    num_cols = len(data[0])
    stats = []
    for col in range(num_cols):
        col_vals = [row[col] for row in data]
        mean = sum(col_vals) / len(col_vals)
        std = math.sqrt(sum((x - mean)**2 for x in col_vals) / len(col_vals))
        stats.append({'min': min(col_vals), 'max': max(col_vals), 'mean': mean, 'std': std})
    return stats

def normalize_row(row, stats, mode):
    norm_row = []
    for i, val in enumerate(row):
        s = stats[i]
        if mode == '1': # Min-Max
            norm_row.append((val - s['min']) / (s['max'] - s['min']) if s['max'] != s['min'] else 0)
        elif mode == '2': # Z-Score
            norm_row.append((val - s['mean']) / s['std'] if s['std'] != 0 else 0)
        else: norm_row.append(val)
    return norm_row

def knn_classifier(X_norm, y, query_norm, k, p):
    results = []
    for i in range(len(X_norm)):
        dist = sum(abs(a - b)**p for a, b in zip(query_norm, X_norm[i]))**(1/p)
        results.append({'id': i + 1, 'norm_feat': X_norm[i], 'label': y[i], 'dist': dist})

    sorted_neighbors = sorted(results, key=lambda x: x['dist'])
    for rank, item in enumerate(sorted_neighbors, 1):
        item['rank'] = rank

    top_k = sorted_neighbors[:k]
    votes = [n['label'] for n in top_k]
    prediction = max(set(votes), key=votes.count) if votes else "N/A"
    return sorted_neighbors, top_k, prediction

def main():
    filename = input("Enter CSV filename: ")
    X_all, y_all = load_data(filename)

    if len(X_all) < 600:
        print("Error: Need at least 600 records (assuming 200 per class).")
        return

    # 1. STRATIFIED SAMPLING (50 per class)
    # Assuming class 1: 0-199, class 2: 200-399, class 3: 400-599
    indices = random.sample(range(0, 200), 50) + \
              random.sample(range(200, 400), 50) + \
              random.sample(range(400, 600), 50)

    X_sampled = [X_all[i] for i in indices]
    y_sampled = [y_all[i] for i in indices]

    # --- NEW: DISPLAY SELECTED 150 RECORDS (ORIGINAL) ---
    print(f"\n--- 1. SELECTED 150 RECORDS (ORIGINAL VALUES) ---")
    print(f"{'No':<4} | {'Original Features':<30} | {'Class'}")
    print("-" * 50)
    for idx, (features, label) in enumerate(zip(X_sampled, y_sampled), 1):
        feat_str = ", ".join([str(f) for f in features])
        print(f"{idx:<4} | {feat_str:<30} | {label}")

    # 2. INPUTS
    query_raw = [float(x) for x in input("\nEnter query values (space separated): ").split()]
    mode = input("Normalization (1:Min-Max, 2:Z-Score, 3:None): ")
    p = float(input("Power 'p' (2 for Euclidean): ") or 2)

    # 3. NORMALIZATION
    stats = get_stats(X_sampled)
    q_norm = normalize_row(query_raw, stats, mode)
    X_norm = [normalize_row(row, stats, mode) for row in X_sampled]

    # 4. ALL SAMPLED RECORDS DISPLAY (WITH DISTANCE)
    all_res, _, _ = knn_classifier(X_norm, y_sampled, q_norm, 1, p)

    print("\n--- 2. SAMPLED RECORDS: NORMALIZED VALUES, DISTANCE AND RANK ---")
    print(f"{'ID':<4} | {'Normalized Features':<35} | {'Distance':<10} | {'Rank'}")
    print("-" * 75)
    # Sort by ID to keep the display consistent with the original selection list
    for r in sorted(all_res, key=lambda x: x['id']):
        norm_str = ", ".join([f"{v:.3f}" for v in r['norm_feat']])
        print(f"{r['id']:<4} | {norm_str:<35} | {r['dist']:.5f}  | {r['rank']}")

    # 5. K-NEIGHBORS DISPLAY
    k = int(input("\nEnter K value for prediction: "))
    _, top_k, final_pred = knn_classifier(X_norm, y_sampled, q_norm, k, p)

    print(f"\n--- 3. TOP {k} NEIGHBORS ---")
    print(f"{'Rank':<5} | {'Original Values':<20} | {'Normalized':<25} | {'Class'}")
    print("-" * 85)
    for item in top_k:
        # item['id'] is 1-based index of X_sampled
        orig_vals = X_sampled[item['id']-1]
        orig_str = ",".join([str(v) for v in orig_vals])
        norm_str = ",".join([f"{v:.3f}" for v in item['norm_feat']])
        print(f"{item['rank']:<5} | {orig_str:<20} | {norm_str:<25} | {item['label']}")

    print(f"\nFINAL PREDICTION: {final_pred}")

if __name__ == "__main__":
    main()

