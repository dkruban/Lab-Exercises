import csv
import math
from collections import Counter

def load_dataset(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data

def entropy_detailed(data, target_attr='play', indent=""):
    values = [row[target_attr] for row in data]
    value_counts = Counter(values)
    total = len(values)

    print(f"Total samples: {total}")
    print(f"Distribution:")
    
    for value, count in value_counts.items():
        print(f"{value}: {count} ({count}/{total})")

    print(f"\nEntropy Formula: H(S) = -Sum[ p(x) * log2(p(x)) ]")
    print(f"Calculation:")
    
    ent = 0.0
    terms = []
    for value, count in value_counts.items():
        probability = count / total
        if probability > 0:
            log_val = math.log2(probability)
            term = probability * log_val
            ent -= term
            terms.append(f"({count}/{total}) * log2({count}/{total})")
            print(f"p({value}) = {count}/{total} = {probability:.4f}")
            print(f"-({probability:.4f}) * log2({probability:.4f})")
            print(f"-({probability:.4f}) * ({log_val:.4f})")
            print(f"-({term:.4f})")
            print(f"= {-term:.4f}")

    print(f"\nH(S) = -[ {' + '.join(terms)} ]")
    print(f"H(S) = {ent:.4f}")
    
    return ent

def entropy_simple(data, target_attr='play'):
    values = [row[target_attr] for row in data]
    value_counts = Counter(values)
    total = len(values)

    ent = 0.0
    for count in value_counts.values():
        probability = count / total
        if probability > 0:
            ent -= probability * math.log2(probability)
    return ent

def information_gain_detailed(data, attribute, target_attr='play'):
    print("\n" + "=" * 70)
    print(f"INFORMATION GAIN CALCULATION FOR: {attribute.upper()}")
    print("=" * 70)
    attr_values = [row[attribute] for row in data]
    attr_counts = Counter(attr_values)
    print(f"\nAttribute '{attribute}' distribution:")
    for value, count in sorted(attr_counts.items()):
        print(f"  {value}: {count} samples")
    print("\n" + "-" * 70)
    print("Step 1: Calculate Entropy of entire dataset H(S)")
    print("-" * 70)
    total_entropy = entropy_detailed(data, target_attr, indent="  ")
    values = sorted(set([row[attribute] for row in data]))
    print("\n" + "-" * 70)
    print(f"Step 2: Calculate Entropy for each value of '{attribute}'")
    print("-" * 70)
    
    weighted_entropy = 0.0
    weighted_terms = []
    subset_entropies = {}
    
    for value in values:
        print(f"\nSubset where {attribute} = '{value}':")
        subset = [row for row in data if row[attribute] == value]
        probability = len(subset) / len(data)
        subset_entropy = entropy_detailed(subset, target_attr, indent="    ")
        subset_entropies[value] = (len(subset), subset_entropy)
        weighted_entropy += probability * subset_entropy
        weighted_terms.append(f"({len(subset)}/{len(data)}) * H({value})")
    print("\n" + "-" * 70)
    print(f"Step 3: Calculate Weighted Average Entropy")
    print("-" * 70)
    
    print(f"\nFormula: H(S, {attribute}) = Sum[ (|Sv|/|S|) * H(Sv) ]")
    print(f"\nCalculation:")
    
    weighted_sum_str = []
    for value in values:
        count, ent = subset_entropies[value]
        prob = count / len(data)
        contribution = prob * ent
        print(f"  ({count}/{len(data)}) * H({value}) = {prob:.4f} * {ent:.4f} = {contribution:.4f}")
        weighted_sum_str.append(f"{contribution:.4f}")
    
    print(f"\n  H(S, {attribute}) = {' + '.join(weighted_sum_str)}")
    print(f"  H(S, {attribute}) = {weighted_entropy:.4f}")
    ig = total_entropy - weighted_entropy
    
    print("\n" + "-" * 70)
    print(f"Step 4: Calculate Information Gain")
    print("-" * 70)
    
    print(f"\nFormula: IG(S, {attribute}) = H(S) - H(S, {attribute})")
    print(f"\nCalculation:")
    print(f"  IG(S, {attribute}) = {total_entropy:.4f} - {weighted_entropy:.4f}")
    print(f"  IG(S, {attribute}) = {ig:.4f}")
    
    return ig

def find_root_node(file_path):
    """Find the best attribute to use as root node"""
    data = load_dataset(file_path)

    print("=" * 70)
    print("DECISION TREE ROOT NODE SELECTION - DETAILED ANALYSIS")
    print("=" * 70)
    print(f"\nDataset: {file_path}")
    print(f"Total samples: {len(data)}")
    
    
    print("\n" + "-" * 70)
    print("DATASET OVERVIEW")
    print("-" * 70)
    
    
    attributes = [key for key in data[0].keys() if key not in ['day', 'play']]
    
    print(f"\nFeature attributes: {attributes}")
    print(f"Target attribute: play")
    
    target_counts = Counter([row['play'] for row in data])
    print(f"\nTarget class distribution:")
    for value, count in target_counts.items():
        percentage = (count / len(data)) * 100
        print(f"  {value}: {count} ({count}/{len(data)} = {percentage:.2f}%)")
    
    # Show distribution for each attribute
    print("\nFeature distributions:")
    for attr in attributes:
        attr_counts = Counter([row[attr] for row in data])
        print(f"\n  {attr}:")
        for value, count in sorted(attr_counts.items()):
            # Also show target distribution for each value
            subset = [row for row in data if row[attr] == value]
            yes_count = sum(1 for row in subset if row['play'] == 'yes')
            no_count = len(subset) - yes_count
            print(f"    {value}: {count} samples (yes: {yes_count}, no: {no_count})")

    # Calculate information gain for each attribute
    gains = {}
    for attr in attributes:
        gains[attr] = information_gain_detailed(data, attr)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY - INFORMATION GAIN COMPARISON")
    print("=" * 70)
    
    print("\n{:<15} {:>15} {:>15} {:>15}".format(
        "Attribute", "H(S)", "H(S,A)", "IG(S,A)"))
    print("-" * 60)
    
    total_ent = entropy_simple(data)
    for attr in sorted(gains.keys(), key=lambda x: gains[x], reverse=True):
        # Recalculate weighted entropy for display
        values = set([row[attr] for row in data])
        weighted_ent = 0.0
        for value in values:
            subset = [row for row in data if row[attr] == value]
            probability = len(subset) / len(data)
            weighted_ent += probability * entropy_simple(subset)
        
        print("{:<15} {:>15.4f} {:>15.4f} {:>15.4f}".format(
            attr, total_ent, weighted_ent, gains[attr]))

    root_node = max(gains, key=gains.get)

    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print(f"\nThe attribute with MAXIMUM Information Gain is: {root_node.upper()}")
    print(f"Information Gain: {gains[root_node]:.4f}")
    print(f"\nTherefore, '{root_node}' should be selected as the ROOT NODE")
    print("of the Decision Tree.")
    print("=" * 70)

    return root_node

if __name__ == "__main__":
    find_root_node('play_tennis.csv')
