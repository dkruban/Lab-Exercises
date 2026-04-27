import math
import random
from collections import Counter

def distance(p1, p2, ch):
    """Calculate distance between two points"""
    if ch == 1:  # Euclidean
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))
    if ch == 2:  # Manhattan
        return sum(abs(a - b) for a, b in zip(p1, p2))

def min_max(data):
    """Normalize data using min-max normalization"""
    cols = list(zip(*data))
    min_vals = [min(c) for c in cols]
    max_vals = [max(c) for c in cols]
    norm_data = []
    for row in data:
        norm_row = [(row[i]-min_vals[i])/(max_vals[i] - min_vals[i]) if max_vals[i] != min_vals[i] else 0
                    for i in range(len(row))]
        norm_data.append(norm_row)
    return norm_data

def get_class_distribution(labels):
    """Get distribution of classes in the dataset"""
    distribution = Counter(labels)
    total = len(labels)
    return distribution, total

def display_distribution(distribution, total, title="CLASS DISTRIBUTION"):
    """Display class distribution with percentages"""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print(f"{'Class':<15} {'Count':<10} {'Percentage':<15}")
    print("-" * 60)
    
    max_count = max(distribution.values()) if distribution else 0
    bar_width = 20
    
    for class_name, count in sorted(distribution.items()):
        percentage = (count / total) * 100 if total > 0 else 0
        print(f"{class_name:<15} {count:<10} {percentage:>6.2f}%")
    
    print("-" * 60)
    print(f"{'Total':<15} {total:<10}")

def knn_classify(train_data, train_labels, test_point, k, distance_metric, weighted=False):
    """
    Classify test_point using KNN
    """
    # Calculate distances to all training points
    distances = []
    for i, train_point in enumerate(train_data):
        dist = distance(train_point, test_point, distance_metric)
        distances.append((dist, train_labels[i], train_point, i))

    # Sort by distance and get k nearest neighbors
    distances.sort(key=lambda x: x[0])
    k_nearest = distances[:k]

    # Store neighbor details for display
    neighbor_details = []
    for rank, (dist, label, train_point, idx) in enumerate(k_nearest, 1):
        neighbor_details.append({
            'rank': rank,
            'features': train_point,
            'class': label,
            'distance': dist,
            'index': idx
        })

    if not weighted:
        # Unweighted: simple majority vote
        votes = {}
        for dist, label, _, _ in k_nearest:
            votes[label] = votes.get(label, 0) + 1
        predicted_class = max(votes, key=votes.get)
    else:
        # Weighted: vote weighted by inverse distance
        votes = {}
        for dist, label, _, _ in k_nearest:
            weight = 1 / (dist**2 + 1e-5)
            votes[label] = votes.get(label, 0) + weight
        predicted_class = max(votes, key=votes.get)

    return predicted_class, neighbor_details

def load_uci_dataset(file_path=None):
    """Load Pima Indians Diabetes dataset from file"""

    if file_path:
        print(f"Loading dataset from local file: {file_path}")
        try:
            with open(file_path, 'r') as f:
                data = f.read()
            lines = data.strip().split('\n')
        except Exception as e:
            print(f"Error reading file: {e}")
            return None, None
    else:
        print("Unable to open file!")
        exit(0)

    try:
        dataset = []
        labels = []

        for line in lines:
            if line.strip():
                parts = line.strip().split(',')
                features = [float(x) for x in parts[:8]]
                dataset.append(features)
                label = 'Positive' if parts[8] == '1' else 'Negative'
                labels.append(label)

        print(f"\nSuccessfully loaded {len(dataset)} samples")
        print(f"Features: Pregnancies, Glucose, BloodPressure, SkinThickness,")
        print(f"          Insulin, BMI, DiabetesPedigree, Age")

        return dataset, labels
    except Exception as e:
        print(f"Error parsing dataset: {e}")
        return None, None

def main():
    print("=" * 60)
    print("KNN CLASSIFIER")
    print("=" * 60)

    print("\nLoad from local file")
    file_path = input("Enter the path to your data file: ").strip()
    dataset, labels = load_uci_dataset(file_path)

    if dataset is None or labels is None:
        print("Failed to load dataset. Exiting...")
        return

    # Show original data distribution
    original_distribution, original_total = get_class_distribution(labels)
    display_distribution(original_distribution, original_total, "ORIGINAL DATA DISTRIBUTION")

    # Get number of records from user
    total_samples = len(dataset)
    print(f"\nTotal available samples: {total_samples}")
    
    while True:
        try:
            num_records = int(input(f"Enter number of records to use (1-{total_samples}): "))
            if 1 <= num_records <= total_samples:
                break
            else:
                print(f"Please enter a number between 1 and {total_samples}")
        except ValueError:
            print("Please enter a valid integer")

    # Random sampling
    if num_records < total_samples:
        indices = random.sample(range(total_samples), num_records)
        dataset = [dataset[i] for i in indices]
        labels = [labels[i] for i in indices]
        print(f"\nRandomly selected {len(dataset)} samples")

    # Show distribution after sampling
    sampled_distribution, sampled_total = get_class_distribution(labels)
    display_distribution(sampled_distribution, sampled_total, "DISTRIBUTION AFTER SAMPLING")

    # Get number of features to use
    total_features = len(dataset[0])
    print(f"\nDataset has {total_features} features")
    num_features = int(input(f"Enter number of features to use (1-{total_features}): "))
    num_features = max(1, min(num_features, total_features))

    # Select features
    print(f"\nSelect {num_features} feature(s) to use:")
    print("Available features:")
    feature_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                     'Insulin', 'BMI', 'DiabetesPedigree', 'Age']
    for i, name in enumerate(feature_names):
        print(f"  {i}: {name}")
    
    selected_features = []
    for i in range(num_features):
        feat_idx = int(input(f"Enter feature index {i+1} (0-{total_features-1}): "))
        selected_features.append(feat_idx)

    # Extract selected features
    train_data = [[row[idx] for idx in selected_features] for row in dataset]

    # Normalize data
    train_data_norm = min_max(train_data)

    # Print normalized data
    print("\n" + "=" * 60)
    print("NORMALIZED DATA")
    print("=" * 60)
    
    # Create header
    header = "S.No\t"
    for i in range(num_features):
        header += f"x{i+1}\t"
    for i in range(num_features):
        header += f"norm{i+1}\t"
    header += "Class"
    print(header)
    print("-" * 60)

    # Print data rows
    for idx, (original, normalized) in enumerate(zip(train_data, train_data_norm), 1):
        row = f"{idx}\t"
        for val in original:
            row += f"{val:.4f}\t"
        for val in normalized:
            row += f"{val:.4f}\t"
        row += labels[idx-1]
        print(row)
    print()

    # Get distance metric
    print("\nSelect distance metric:")
    print("1. Euclidean")
    print("2. Manhattan")
    distance_metric = int(input("Enter choice (1 or 2): "))

    # Get k value
    k = int(input(f"\nEnter k value (1-{len(dataset)}): "))
    k = max(1, min(k, len(dataset)))

    # Get weighted/unweighted choice
    print("\nSelect KNN type:")
    print("1. Unweighted")
    print("2. Weighted")
    weighted_choice = int(input("Enter choice (1 or 2): "))
    weighted = (weighted_choice == 2)

    # Get test point
    print(f"\nEnter test point ({num_features} values):")
    test_point = []
    for i in range(num_features):
        feat_name = feature_names[selected_features[i]]
        val = float(input(f"Feature {selected_features[i]} ({feat_name}) value: "))
        test_point.append(val)

    # Normalize test point
    cols = list(zip(*train_data))
    min_vals = [min(c) for c in cols]
    max_vals = [max(c) for c in cols]
    test_point_norm = [(test_point[i]-min_vals[i])/(max_vals[i] - min_vals[i]) if max_vals[i] != min_vals[i] else 0
                       for i in range(len(test_point))]

    # Calculate distances for all points
    all_distances = []
    for i, train_point in enumerate(train_data_norm):
        dist = distance(train_point, test_point_norm, distance_metric)
        all_distances.append((i, train_point, labels[i], dist))

    # Sort by distance to get ranks
    sorted_by_distance = sorted(all_distances, key=lambda x: x[3])
    ranks = {item[0]: rank + 1 for rank, item in enumerate(sorted_by_distance)}

    # Display distances table
    print("\n" + "=" * 60)
    print("DISTANCES FROM TEST POINT")
    print("=" * 60)
    print(f"Test Point (Original): {test_point}")
    print(f"Test Point (Normalized): {[f'{v:.4f}' for v in test_point_norm]}")
    print(f"Distance Metric: {'Euclidean' if distance_metric == 1 else 'Manhattan'}")
    print()

    header = "S.No"
    for i in range(num_features):
        header += f"\tnorm{i+1}"
    header += "\tClass\tDistance\tRank"
    print(header)
    print("-" * 60)

    for i, train_point, label, dist in all_distances:
        row = f"{i+1}"
        for feat_val in train_point:
            row += f"\t{feat_val:.4f}"
        row += f"\t{label}\t{dist:.4f}\t{ranks[i]}"
        print(row)

    # Classify
    predicted_class, neighbor_details = knn_classify(train_data_norm, labels, test_point_norm, k, distance_metric, weighted)

    # Display result
    print("\n" + "=" * 60)
    print("CLASSIFICATION RESULT")
    print("=" * 60)
    print(f"Test Point: {test_point}")
    print(f"Features Used: {[feature_names[i] for i in selected_features]}")
    print(f"Distance Metric: {'Euclidean' if distance_metric == 1 else 'Manhattan'}")
    print(f"K Value: {k}")
    print(f"KNN Type: {'Weighted' if weighted else 'Unweighted'}")

    # Print k-nearest neighbors table
    print("\n" + "=" * 60)
    print(f"K-NEAREST NEIGHBORS (k={k})")
    print("=" * 60)

    neighbor_details.sort(key=lambda x: x['rank'])

    header = "Rank"
    for i in range(num_features):
        header += f"\tnorm{i+1}"
    header += "\tClass\tDistance"
    if weighted:
        header += "\tWeight"
    print(header)
    print("-" * 60)

    for neighbor in neighbor_details:
        row = f"{neighbor['rank']}"
        for feat_val in neighbor['features']:
            row += f"\t{feat_val:.4f}"
        row += f"\t{neighbor['class']}\t{neighbor['distance']:.4f}"
        if weighted:
            weight = 1 / (neighbor['distance']**2 + 1e-5)
            row += f"\t{weight:.4f}"
        print(row)

    # Show voting summary
    print("\n" + "=" * 60)
    print("VOTING SUMMARY")
    print("=" * 60)
    
    # Show class distribution in k-nearest neighbors
    neighbor_classes = [n['class'] for n in neighbor_details]
    neighbor_distribution = Counter(neighbor_classes)
    print(f"\nClass distribution in {k} nearest neighbors:")
    for class_name, count in sorted(neighbor_distribution.items()):
        percentage = (count / k) * 100
        print(f"  {class_name}: {count} ({percentage:.1f}%)")
    
    if weighted:
        votes = {}
        for neighbor in neighbor_details:
            label = neighbor['class']
            weight = 1 / (neighbor['distance']**2 + 1e-5)
            votes[label] = votes.get(label, 0) + weight
        print("\nWeighted votes:")
        total_weight = sum(votes.values())
        for label, vote in sorted(votes.items()):
            percentage = (vote / total_weight) * 100
            print(f"  {label}: {vote:.4f} ({percentage:.1f}%)")
    else:
        votes = {}
        for neighbor in neighbor_details:
            label = neighbor['class']
            votes[label] = votes.get(label, 0) + 1
        print("\nVote counts:")
        for label, vote in sorted(votes.items()):
            percentage = (vote / k) * 100
            print(f"  {label}: {vote} ({percentage:.1f}%)")

    print("\n" + "=" * 60)
    print(f"PREDICTED CLASS: {predicted_class}")
    print("=" * 60)

if __name__ == "__main__":
    main()
