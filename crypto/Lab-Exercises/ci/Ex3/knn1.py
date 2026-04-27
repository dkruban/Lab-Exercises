import math
import random
import urllib.request

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

def knn_classify(train_data, train_labels, test_point, k, distance_metric, weighted=False):
    """
    Classify test_point using KNN
    train_data: list of training points (normalized)
    train_labels: list of class labels
    test_point: point to classify
    k: number of neighbors
    distance_metric: 1 for Euclidean, 2 for Manhattan
    weighted: True for weighted KNN, False for unweighted
    Returns: (predicted_class, neighbor_details)
    """
    # Calculate distances to all training points
    distances = []
    for i, train_point in enumerate(train_data):
        dist = distance(train_point, test_point, distance_metric)
        distances.append((dist, train_labels[i], train_point, i))
    
    # Sort by distance and get k nearest neighbors
    distances.sort(key=lambda x: x[0])
    k_nearest = distances[:k]
    
    # Store neighbor details for display (in original data order, not sorted by distance)
    neighbor_details = []
    for rank, (dist, label, train_point, idx) in enumerate(k_nearest, 1):
        neighbor_details.append({
            'rank': rank,
            'features': train_point,
            'class': label,
            'distance': dist,
            'index': idx
        })
    
    # Sort by original index instead of distance for display
    neighbor_details.sort(key=lambda x: x['index'])
    
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
            # Avoid division by zero for exact matches
            weight = 1 / (dist**2 + 1e-5)
            votes[label] = votes.get(label, 0) + weight
        predicted_class = max(votes, key=votes.get)
    
    return predicted_class, neighbor_details

def load_uci_dataset(file_path=None):
    """Load Pima Indians Diabetes dataset from file or UCI Machine Learning Repository (Binary Classification)"""
    
    if file_path:
        # Load from local file
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
            if line.strip():  # Skip empty lines
                parts = line.strip().split(',')
                # Extract features (first 8 columns)
                features = [float(x) for x in parts[:8]]
                dataset.append(features)
                # Extract label (last column): 0 = No diabetes, 1 = Diabetes
                label = 'Positive' if parts[8] == '1' else 'Negative'
                labels.append(label)
        
        print(f"Successfully loaded {len(dataset)} samples")
        print("Dataset description: ")
        print(f"Features: Pregnancies, Glucose, BloodPressure, SkinThickness,")
        print(f"          Insulin, BMI, DiabetesPedigree, Age")
        print(f"Classes: {set(labels)} (Positive=Diabetes, Negative=No Diabetes)")
        print(f"Class distribution: Positive={labels.count('Positive')}, Negative={labels.count('Negative')}\n")
        
        return dataset, labels
    except Exception as e:
        print(f"Error parsing dataset: {e}")
        return None, None

def main():
    print("=" * 50)
    print("KNN CLASSIFIER")
    print("=" * 50)
    
    print("Load from local file")
    file_path = input("Enter the path to your data file: ").strip()
    dataset, labels = load_uci_dataset(file_path)
    
    if dataset is None or labels is None:
        print("Failed to load dataset. Exiting...")
        return
    
    # Randomly select 50 points from the dataset
    total_samples = len(dataset)
    if total_samples > 50:
        print(f"\nRandomly selecting 50 samples from {total_samples} total samples...")
        indices = random.sample(range(total_samples), 50)
        dataset = [dataset[i] for i in indices]
        labels = [labels[i] for i in indices]
        print(f"Using {len(dataset)} samples for training and classification\n")
    else:
        print(f"Dataset has {total_samples} samples (less than 50), using all samples\n")
    
    # Get number of features to use
    total_features = len(dataset[0])
    print(f"\nDataset has {total_features} features")
    num_features = int(input(f"Enter number of features to use (1-{total_features}): "))
    num_features = max(1, min(num_features, total_features))
    
    # Select features
    print(f"\nSelect {num_features} feature(s) to use:")
    selected_features = []
    for i in range(num_features):
        feat_idx = int(input(f"Enter feature index {i+1} (0-{total_features-1}): "))
        selected_features.append(feat_idx)
    
    # Extract selected features
    train_data = [[row[idx] for idx in selected_features] for row in dataset]
    
    # Normalize data
    train_data_norm = min_max(train_data)
    
    # Print normalized data
    print("\n" + "=" * 50)
    print("NORMALIZED DATA")
    print("=" * 50)
    # Create header: x1 x2 ... xn norm1 norm2 ... normn
    header = ""
    for i in range(num_features):
        header += f"x{i+1}\t"
    for i in range(num_features):
        header += f"norm{i+1}\t"
    print(header.rstrip())
    print("-" * len(header.expandtabs()))
    
    # Print data rows
    for idx, (original, normalized) in enumerate(zip(train_data, train_data_norm), 1):
        row = ""
        # Original values
        for val in original:
            row += f"{val:.4f}\t"
        # Normalized values
        for val in normalized:
            row += f"{val:.4f}\t"
        print(row.rstrip())
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
        val = float(input(f"Feature {selected_features[i]} value: "))
        test_point.append(val)
    
    # Normalize test point using same min-max values
    cols = list(zip(*train_data))
    min_vals = [min(c) for c in cols]
    max_vals = [max(c) for c in cols]
    test_point_norm = [(test_point[i]-min_vals[i])/(max_vals[i] - min_vals[i]) if max_vals[i] != min_vals[i] else 0 
                       for i in range(len(test_point))]
    
    print("DISTANCES")
    print("=" * 50)
    header = "S.No"
    for i in range(num_features):
        header+= f"\t{selected_features[i]}"
    header+="\tDistance\tRank"
    print(header)
    row = ""
    for i in range(len(train_data_norm)):
        print(f"{i+1}", end="")
        for j in range(len(selected_features)):
            print(f"\t{train_data_norm[i][selected_features[j]]}", end="");
        print(f"\t{}")
        
    

    # Classify
    predicted_class, neighbor_details = knn_classify(train_data_norm, labels, test_point_norm, k, distance_metric, weighted)
    
    # Display result
    print("\n" + "=" * 50)
    print("CLASSIFICATION RESULT")
    print("=" * 50)
    print(f"Test Point: {test_point}")
    print(f"Features Used: {selected_features}")
    print(f"Distance Metric: {'Euclidean' if distance_metric == 1 else 'Manhattan'}")
    print(f"K Value: {k}")
    print(f"KNN Type: {'Weighted' if weighted else 'Unweighted'}")
    
    # Print k-nearest neighbors table
    print("\n" + "=" * 50)
    print("K-NEAREST NEIGHBORS")
    print("=" * 50)
    
    # Create table header
    header = "S.No"
    for i in range(num_features):
        header += f"\tFeature {i+1}"
    header += "\tClass\tDistance\tRank"
    print(header)
    print("-" * len(header.expandtabs()))
    
    # Print each neighbor
    for neighbor in neighbor_details:
        row = f"{neighbor['rank']}"
        for feat_val in neighbor['features']:
            row += f"\t{feat_val:.4f}"
        row += f"\t{neighbor['class']}\t{neighbor['distance']:.4f}\t{neighbor['rank']}"
        print(row)
    
    print("\n" + "=" * 50)
    print(f"Predicted Class: {predicted_class}")
    print("=" * 50)

if __name__ == "__main__":
    main()

