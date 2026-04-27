import csv
import math
from collections import Counter


class TreeNode:
    def __init__(self, attribute=None, label=None, depth=0):
        self.attribute = attribute
        self.label = label
        self.children = {}
        self.depth = depth
        self.data_count = 0
        self.class_dist = {}
        self.entropy = 0.0
        self.info_gain = 0.0


def print_table(headers, rows, indent=""):
    str_rows = [[str(cell) for cell in row] for row in rows]
    str_headers = [str(h) for h in headers]
    cols = list(zip(*([str_headers] + str_rows))) if rows else [[h] for h in str_headers]
    widths = [max(len(item) for item in col) for col in cols]

    def fmt_row(row):
        return " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(row))

    print(indent + fmt_row(str_headers))
    print(indent + "-+-".join("-" * w for w in widths))
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
    if not data:
        if show_steps:
            print(f"{indent}No data - Entropy: 0.0")
        return 0.0

    counts = Counter(row[target_attr] for row in data)
    total = len(data)

    entropy_val = 0.0
    parts = []
    for cls, count in sorted(counts.items()):
        prob = count / total
        if prob > 0:
            entropy_val -= prob * math.log2(prob)
            parts.append(f"-({count}/{total})*log2({count}/{total})")

    if show_steps:
        dist_rows = [[cls, count, f"{count/total:.4f}"] for cls, count in sorted(counts.items())]
        print(f"{indent}Total samples: {total}")
        print(f"{indent}Class Distribution:")
        print_table(["Class", "Count", "Probability"], dist_rows, indent=indent + "  ")
        if parts:
            print(f"{indent}Entropy = {' '.join(parts)}")
        print(f"{indent}Entropy = {entropy_val:.4f}")

    return entropy_val


def calculate_ig(data, attribute, target_attr, parent_entropy, show_steps=False, indent=""):
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
        dist_str = ", ".join(f"{k}:{v}" for k, v in sorted(dist.items()))
        split_rows.append([val, len(subset), dist_str, f"{sub_entropy:.4f}", f"{weight:.4f}"])
        split_details.append(f"({len(subset)}/{total}*{sub_entropy:.4f})")

    ig = parent_entropy - weighted_entropy

    if show_steps:
        print(f"\n{indent}Attribute: {attribute}")
        print(f"{indent}  Split Summary:")
        print_table(["Value", "Count", "Class Dist", "Entropy", "Weight"], split_rows, indent=indent + "    ")
        print(f"{indent}  Weighted Entropy = {' + '.join(split_details)}")
        print(f"{indent}                   = {weighted_entropy:.4f}")
        print(f"{indent}  Information Gain = {parent_entropy:.4f} - {weighted_entropy:.4f} = {ig:.4f}")

    return ig


def build_tree(data, attributes, target_attr, depth=0, show_steps=False, max_depth=None, parent_attr=None, parent_val=None):
    indent = "    " * depth
    branch_info = f" (Branch: {parent_attr}={parent_val})" if parent_attr else ""
    
    if show_steps:
        print(f"\n{'='*70}")
        print(f"{indent}NODE AT DEPTH {depth}{branch_info}")
        print(f"{indent}Samples: {len(data)}")
    
    node = TreeNode(depth=depth)
    node.data_count = len(data)
    node.class_dist = dict(Counter(row[target_attr] for row in data))
    
    if show_steps and data:
        dist_str = ", ".join(f"{k}:{v}" for k, v in sorted(node.class_dist.items()))
        print(f"{indent}Class Distribution: [{dist_str}]")
    
    if not data:
        node.label = "Unknown"
        if show_steps:
            print(f"{indent}No data remaining")
            print(f"{indent}LEAF NODE: Unknown")
        return node
    
    classes = set(row[target_attr] for row in data)
    if len(classes) == 1:
        node.label = list(classes)[0]
        node.entropy = 0.0
        if show_steps:
            print(f"{indent}Pure node - all samples belong to class '{node.label}'")
            print(f"{indent}LEAF NODE: {node.label}")
        return node
    
    if not attributes:
        counts = Counter(row[target_attr] for row in data)
        node.label = counts.most_common(1)[0][0]
        if show_steps:
            print(f"{indent}No attributes remaining")
            print(f"{indent}LEAF NODE (majority vote): {node.label}")
        return node
    
    if max_depth is not None and depth >= max_depth:
        counts = Counter(row[target_attr] for row in data)
        node.label = counts.most_common(1)[0][0]
        if show_steps:
            print(f"{indent}Maximum depth ({max_depth}) reached")
            print(f"{indent}LEAF NODE (majority vote): {node.label}")
        return node
    
    if show_steps:
        print(f"\n{indent}Computing Parent Entropy:")
    
    parent_entropy = calculate_entropy(data, target_attr, show_steps=show_steps, indent=indent + "  ")
    node.entropy = parent_entropy
    
    if show_steps:
        print(f"\n{indent}Computing Information Gain for {len(attributes)} attribute(s)")
        print(f"{indent}Available attributes: {attributes}")
    
    gains = {}
    for attr in attributes:
        gains[attr] = calculate_ig(data, attr, target_attr, parent_entropy,
                                   show_steps=show_steps, indent=indent + "  ")
    
    best_attr = max(gains, key=gains.get)
    best_gain = gains[best_attr]
    
    if show_steps:
        print(f"\n{indent}INFORMATION GAIN SUMMARY:")
        gain_rows = [[attr, f"{gains[attr]:.4f}", "<-- BEST" if attr == best_attr else ""] 
                     for attr in sorted(gains.keys(), key=lambda x: gains[x], reverse=True)]
        print_table(["Attribute", "Info Gain", ""], gain_rows, indent=indent + "  ")
        print(f"\n{indent}SELECTED: {best_attr} (Information Gain = {best_gain:.4f})")
    
    node.attribute = best_attr
    node.info_gain = best_gain
    
    values = sorted(set(row[best_attr] for row in data))
    remaining_attrs = [a for a in attributes if a != best_attr]
    
    if show_steps:
        print(f"\n{indent}Creating branches for '{best_attr}': {values}")
        print(f"{indent}Remaining attributes for children: {remaining_attrs if remaining_attrs else 'None'}")
    
    for val in values:
        subset = [row for row in data if row[best_attr] == val]
        
        if show_steps:
            print(f"\n{indent}Branch: {best_attr} = '{val}' (Subset size: {len(subset)})")
        
        if not subset:
            counts = Counter(row[target_attr] for row in data)
            child = TreeNode(depth=depth + 1)
            child.label = counts.most_common(1)[0][0]
            child.data_count = 0
            child.class_dist = {}
            if show_steps:
                print(f"{indent}  Empty subset - using parent majority: {child.label}")
        else:
            child = build_tree(subset, remaining_attrs, target_attr,
                               depth=depth + 1, show_steps=show_steps, max_depth=max_depth,
                               parent_attr=best_attr, parent_val=val)
        
        node.children[val] = child
    
    return node


def print_tree(node, prefix="", is_last=True, attr_value=None, is_root=True):
    if is_root:
        if node.label is not None:
            dist_str = ", ".join(f"{k}:{v}" for k, v in sorted(node.class_dist.items()))
            print(f"ROOT -> [{node.label}] ({dist_str})")
        else:
            dist_str = ", ".join(f"{k}:{v}" for k, v in sorted(node.class_dist.items()))
            print(f"ROOT: [{node.attribute}?] (n={node.data_count}, {dist_str})")
            print(f"|     Entropy={node.entropy:.4f}, InfoGain={node.info_gain:.4f}")
            
            children = list(node.children.items())
            for i, (val, child) in enumerate(children):
                is_last_child = (i == len(children) - 1)
                print_tree(child, "", is_last_child, val, is_root=False)
    else:
        connector = "+-- " if is_last else "|-- "
        extension = "    " if is_last else "|   "
        
        branch_label = f"[{attr_value}] " if attr_value is not None else ""
        
        if node.label is not None:
            dist_str = ", ".join(f"{k}:{v}" for k, v in sorted(node.class_dist.items())) if node.class_dist else "n=0"
            print(f"{prefix}{connector}{branch_label}-> LEAF: {node.label} ({dist_str})")
        else:
            dist_str = ", ".join(f"{k}:{v}" for k, v in sorted(node.class_dist.items()))
            print(f"{prefix}{connector}{branch_label}[{node.attribute}?] (n={node.data_count}, {dist_str})")
            print(f"{prefix}{extension}    Entropy={node.entropy:.4f}, InfoGain={node.info_gain:.4f}")
            
            children = list(node.children.items())
            for i, (val, child) in enumerate(children):
                is_last_child = (i == len(children) - 1)
                print_tree(child, prefix + extension, is_last_child, val, is_root=False)


def print_rules(node, conditions=None, rule_num=None):
    if conditions is None:
        conditions = []
    if rule_num is None:
        rule_num = [1]
    
    if node.label is not None:
        if conditions:
            cond_str = " AND ".join(conditions)
            print(f"  Rule {rule_num[0]}: IF {cond_str} THEN {node.label}")
        else:
            print(f"  Rule {rule_num[0]}: (Default) -> {node.label}")
        rule_num[0] += 1
    else:
        for val, child in sorted(node.children.items()):
            new_conditions = conditions + [f"{node.attribute}='{val}'"]
            print_rules(child, new_conditions, rule_num)


def get_tree_stats(node, stats=None):
    if stats is None:
        stats = {'depth': 0, 'nodes': 0, 'leaves': 0, 'internal': 0}
    
    stats['nodes'] += 1
    stats['depth'] = max(stats['depth'], node.depth)
    
    if node.label is not None:
        stats['leaves'] += 1
    else:
        stats['internal'] += 1
        for child in node.children.values():
            get_tree_stats(child, stats)
    
    return stats


def predict(node, instance):
    if node.label is not None:
        return node.label
    
    attr_value = instance.get(node.attribute)
    if attr_value in node.children:
        return predict(node.children[attr_value], instance)
    else:
        if node.class_dist:
            return max(node.class_dist, key=node.class_dist.get)
        return "Unknown"


def main():
    print("=" * 70)
    print("DECISION TREE BUILDER (ID3 Algorithm)")
    print("=" * 70)

    filename_input = input("\nEnter CSV file name (or Enter for default): ").strip()
    if not filename_input:
        filename = 'play_tennis.csv'
    else:
        filename = filename_input

    data = load_dataset(filename)

    if not data:
        alt_paths = ['Ex4/play_tennis.csv', 'data/play_tennis.csv']
        for alt in alt_paths:
            data = load_dataset(alt)
            if data:
                filename = alt
                break
        
        if not data:
            print("Could not load data. Exiting.")
            return

    headers = list(data[0].keys())
    preview_rows = [[row[h] for h in headers] for row in data[:10]]
    print(f"\nDataset Preview ({min(10, len(data))} of {len(data)} rows):")
    print_table(headers, preview_rows, indent="  ")

    print(f"\nColumns: {headers}")

    target_input = input(f"Target attribute (default: '{headers[-1]}'): ").strip()
    target = target_input if target_input else headers[-1]

    if target not in headers:
        print(f"Error: Target '{target}' not found")
        return

    to_ignore = input("Columns to ignore (comma-separated, or Enter to skip): ").strip()
    ignore_list = [x.strip() for x in to_ignore.split(',')] if to_ignore else []

    max_depth_input = input("Max depth (or Enter for unlimited): ").strip()
    max_depth = int(max_depth_input) if max_depth_input.isdigit() else None

    attributes = [col for col in headers if col != target and col not in ignore_list]

    print("\n" + "=" * 70)
    print("CONFIGURATION")
    print("=" * 70)
    print(f"  Dataset:    {filename} ({len(data)} samples)")
    print(f"  Target:     {target}")
    print(f"  Attributes: {attributes}")
    print(f"  Ignored:    {ignore_list if ignore_list else 'None'}")
    print(f"  Max Depth:  {max_depth if max_depth else 'Unlimited'}")

    show_steps = input("\nShow detailed steps? (y/n, default: y): ").strip().lower()
    show_steps = show_steps != 'n'

    input("\nPress Enter to build tree...")

    print("\n" + "#" * 70)
    print("BUILDING DECISION TREE")
    print("#" * 70)
    
    tree = build_tree(data, attributes, target, depth=0, show_steps=show_steps, max_depth=max_depth)
    
    print("\n" + "#" * 70)
    print("FINAL DECISION TREE")
    print("#" * 70)
    print()
    print_tree(tree)
    
    stats = get_tree_stats(tree)
    print("\n" + "-" * 70)
    print("TREE STATISTICS:")
    print(f"  Total Nodes:    {stats['nodes']}")
    print(f"  Internal Nodes: {stats['internal']}")
    print(f"  Leaf Nodes:     {stats['leaves']}")
    print(f"  Maximum Depth:  {stats['depth']}")
    
    print("\n" + "#" * 70)
    print("DECISION RULES")
    print("#" * 70)
    print()
    print_rules(tree)
    
    correct = sum(1 for row in data if predict(tree, row) == row[target])
    accuracy = correct / len(data) if data else 0
    print("\n" + "-" * 70)
    print(f"Training Accuracy: {accuracy * 100:.2f}% ({correct}/{len(data)})")
    
    while True:
        test = input("\nTest new instance? (y/n): ").strip().lower()
        if test != 'y':
            break
        
        instance = {}
        for attr in attributes:
            vals = sorted(set(row[attr] for row in data))
            instance[attr] = input(f"  {attr} {vals}: ").strip()
        
        result = predict(tree, instance)
        print(f"\n  Prediction: {target} = {result}")
    
    print("\nDone.")


if __name__ == "__main__":
    main()
