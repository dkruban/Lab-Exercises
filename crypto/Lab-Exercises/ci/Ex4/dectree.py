import csv
import math
from collections import Counter

def load_dataset(file_path):
    """Load the play tennis dataset from CSV file"""
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data

def entropy(data, target_attr='play'):
    """Calculate entropy of the dataset"""
    values = [row[target_attr] for row in data]
    value_counts = Counter(values)
    total = len(values)
    
    ent = 0.0
    for count in value_counts.keys():
        print(count+":",value_counts[count])
        probability = value_counts[count] / total
        if probability > 0:
            ent -= probability * math.log2(probability)
    
    return ent

def information_gain(data, attribute, target_attr='play'):
    """Calculate information gain for a given attribute"""
    # Calculate entropy of entire dataset
    print("Entropy of ",attribute)
    total_entropy = entropy(data, target_attr)
    
    # Get unique values for this attribute
    values = set([row[attribute] for row in data])
    
    # Calculate weighted entropy for each value
    weighted_entropy = 0.0
    for value in values:
        print(value)
        subset = [row for row in data if row[attribute] == value]
        probability = len(subset) / len(data)
        weighted_entropy += probability * entropy(subset, target_attr)
    
    # Information gain is the reduction in entropy
    return total_entropy - weighted_entropy

def find_root_node(file_path):
    """Find the best attribute to use as root node"""
    # Load dataset
    data = load_dataset(file_path)
    
    # Get all attributes except 'day' and 'play' (target)
    attributes = [key for key in data[0].keys() if key not in ['day', 'play']]
    
    # Calculate information gain for each attribute
    gains = {}
    for attr in attributes:
        gains[attr] = information_gain(data, attr)
    
    # Display results
    print("=" * 60)
    print("DECISION TREE ROOT NODE SELECTION")
    print("=" * 60)
    print(f"\nDataset: {file_path}")
    print(f"Total samples: {len(data)}")
    print(f"\nEntropy of dataset: {entropy(data):.4f}")
    print("\n" + "-" * 60)
    print("Information Gain for each attribute:")
    print("-" * 60)
    
    for attr in sorted(gains.keys(), key=lambda x: gains[x], reverse=True):
        print(f"{attr:15s}: {gains[attr]:.4f}")
    
    # Find attribute with maximum information gain
    root_node = max(gains, key=gains.get)
    
    print("\n" + "=" * 60)
    print(f"ROOT NODE: {root_node}")
    print(f"Information Gain: {gains[root_node]:.4f}")
    print("=" * 60)
    
    return root_node

if __name__ == "__main__":
    find_root_node('play_tennis.csv')
