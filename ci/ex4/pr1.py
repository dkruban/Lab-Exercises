import numpy as np
from collections import Counter

df = pd.read_csv('input.txt')

def calculate_entropy(data):
    class_counts = Counter(data['PlayTennis'])
    total = len(data)
    entropy = 0
    for count in class_counts.values():
        probability = count / total
        entropy -= probability * np.log2(probability)
    return entropy

def calculate_information_gain_with_steps(df, attribute):
    total_entropy = calculate_entropy(df)
    print(f"\nAttribute: {attribute}")
    print(f"Total Entropy: {total_entropy:.4f}")

    values, counts = np.unique(df[attribute], return_counts=True)
    weighted_entropy = 0

    for value, count in zip(values, counts):
        subset = df[df[attribute] == value]
        subset_entropy = calculate_entropy(subset)
        weight = count / len(df)
        weighted_entropy += weight * subset_entropy

    information_gain = total_entropy - weighted_entropy
    print(f"Weighted Entropy: {weighted_entropy:.4f}")
    print(f"Information Gain: {information_gain:.4f}")
    return information_gain

total_entropy = calculate_entropy(df)
print(f"Overall Dataset Entropy: {total_entropy:.4f}\n")

attributes = ['Outlook', 'Temp', 'Humidity', 'Wind']
information_gains = {}
for attr in attributes:
    gain = calculate_information_gain_with_steps(df, attr)
    information_gains[attr] = gain

best_root = max(information_gains, key=information_gains.get)
print(f"\nBest Root Node: {best_root} with Information Gain: {information_gains[best_root]:.4f}")
