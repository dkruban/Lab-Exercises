
import csv
import math
from collections import Counter

def print_table(headers, rows, indent=""):
    """Print a simple text table with aligned columns."""
    # Convert all to strings
    str_rows = [[str(cell) for cell in row] for row in rows]
    str_headers = [str(h) for h in headers]
    cols = list(zip(*([str_headers] + str_rows))) if rows else [[h] for h in str_headers]
    widths = [max(len(item) for item in col) for col in cols]

    def fmt_row(row):
        return " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(row))

    header_line = fmt_row(str_headers)
    sep_line = "-+-".join("-" * w for w in widths)

    print(indent + header_line)
    print(indent + sep_line)
    for row in str_rows:
        print(indent + fmt_row(row))

def load_dataset(file_path):
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

def calculate_entropy(data, target_attr, show_steps=False, indent=""):
    """Calculates Entropy for a dataset."""
    counts = Counter(row[target_attr] for row in data)
    total = len(data)

    entropy_val = 0.0
    parts = []
    for cls, count in counts.items():
        prob = count / total
        if prob > 0:
            entropy_val -= prob * math.log2(prob)
            parts.append(f"-({count}/{total})*log2({count}/{total})")

    if show_steps:
        dist_rows = [[cls, count] for cls, count in sorted(counts.items())]
        print(f"{indent}Total: {total}")
        print(f"{indent}Class Distribution:")
        print_table(["Class", "Count"], dist_rows, indent=indent + "  ")
        print(f"{indent}Entropy Formula: {' + '.join(parts)}")
        print(f"{indent}Entropy: {entropy_val:.4f}")

    return entropy_val

def calculate_ig(data, attribute, target_attr, parent_entropy, show_steps=False):
    """Calculates Information Gain for an attribute."""
    values = sorted(set(row[attribute] for row in data))
    total = len(data)

    weighted_entropy = 0.0
    split_rows = []
    split_details = []

    for val in values:
        subset = [row for row in data if row[attribute] == val]
        weight = len(subset) / total
        sub_entropy = calculate_entropy(subset, target_attr)
        weighted_entropy += weight * sub_entropy

        dist = Counter(row[target_attr] for row in subset)
        dist_str = ", ".join(f"{k}:{v}" for k, v in dist.items())
        split_rows.append([val, len(subset), dist_str, f"{sub_entropy:.4f}", f"{weight:.4f}"])
        split_details.append(f"({len(subset)}/{total} * {sub_entropy:.4f})")

    ig = parent_entropy - weighted_entropy

    if show_steps:
        print(f"\nAttribute: {attribute}")
        print("  Split Summary:")
        print_table(["Value", "Count", "Class Dist", "Entropy", "Weight"], split_rows, indent="  ")
        print(f"  Weighted Entropy: {' + '.join(split_details)} = {weighted_entropy:.4f}")
        print(f"  Information Gain: {parent_entropy:.4f} - {weighted_entropy:.4f} = {ig:.4f}")

    return ig

def summarize_split(data, attribute, target_attr):
    """Creates a simple summary table for a root split."""
    values = sorted(set(row[attribute] for row in data))
    rows = []
    for val in values:
        subset = [row for row in data if row[attribute] == val]
        dist = Counter(row[target_attr] for row in subset)
        dist_str = ", ".join(f"{k}:{v}" for k, v in dist.items())
        rows.append([val, len(subset), dist_str])
    return rows

def find_root_node(data, attributes, target_attr):
    """Finds the best root attribute using information gain."""
    parent_entropy = calculate_entropy(data, target_attr)
    gains = {attr: calculate_ig(data, attr, target_attr, parent_entropy) for attr in attributes}
    best_attr = max(gains, key=gains.get)
    return best_attr, gains, parent_entropy

def main():
    print("Decision Tree root node")
    print("---------------------------------------")
    
    # Ask for filename
    filename_input = input("Enter the CSV file name: ").strip()
    if not filename_input:
         filename = 'Ex4/play_tennis.csv' 
    else:
         filename = filename_input
         
    data = load_dataset(filename)
    
    if not data:
        print("Trying to load from current directory...")
        # Fallback to local if Ex4 prefix failed or vice versa
        if filename.startswith("Ex4/"):
             alt_filename = filename.replace("Ex4/", "")
             data = load_dataset(alt_filename)
        elif not filename_input: # If default failed, try local play_tennis.csv
             data = load_dataset("play_tennis.csv")
             
        if not data:
             print("Could not load data. Exiting.")
             return

    # Dataset preview table (notebook-like)
    headers = list(data[0].keys())
    preview_rows = [[row[h] for h in headers] for row in data[:10]]
    print("\nDataset Preview (first 10 rows):")
    print_table(headers, preview_rows, indent="  ")

    # Infer header
    print(f"\nColumns found: {headers}")
    
    # Ask for target attribute
    target_input = input(f"Enter target attribute (default is last column '{headers[-1]}'): ").strip()
    target = target_input if target_input else headers[-1]
    
    if target not in headers:
        print(f"Error: Target '{target}' not found in columns: {headers}")
        return

    # Ask for non-attributes (ID columns) to ignore
    print(f"Select columns to IGNORE as attributes (e.g. IDs).")
    to_ignore = input("Enter column names separated by comma (or press Enter to skip): ").strip()
    ignore_list = [x.strip() for x in to_ignore.split(',')] if to_ignore else []
    
    # Filter attributes
    attributes = [col for col in headers if col != target and col not in ignore_list]

    print("\n" + "="*80)
    print("CONFIGURATION")
    print(f"  Dataset: {filename}")
    print(f"  Target: {target}")
    print(f"  Attributes: {attributes}")
    print(f"  Ignored: {ignore_list}")
    print("="*80)
    
    input("Press Enter to analyze the root node...")

    best_attr, gains, parent_entropy = find_root_node(data, attributes, target)

    print("\n" + "#"*80)
    print("ROOT NODE DETAILS")
    print("#"*80)
    print("Parent Entropy:")
    calculate_entropy(data, target, show_steps=True, indent="  ")

    print("\nStep-by-step Information Gain for Each Attribute:")
    for attr in attributes:
        calculate_ig(data, attr, target, parent_entropy, show_steps=True)

    print("\nSummary:")
    gain_rows = [[attr, f"{gains[attr]:.4f}"] for attr in sorted(gains.keys())]
    print_table(["Attribute", "Information Gain"], gain_rows, indent="  ")

    print(f"\nSelected Root Attribute: {best_attr}")
    print("\nRoot Split Overview:")
    split_rows = summarize_split(data, best_attr, target)
    print_table(["Value", "Count", "Class Dist"], split_rows, indent="  ")
    print("#"*80)

if __name__ == "__main__":
    main()

