import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from tabulate import tabulate

# Get user inputs
dataset_path = input("Enter dataset path: ")
n_estimators = int(input("Enter number of decision trees: "))
target_col = input("Enter target column name: ")
n_splits = int(input("Enter number of splits (folds): "))

# Load dataset
df = pd.read_csv(dataset_path)
df.columns = df.columns.str.strip()
target_col = target_col.strip()

if target_col not in df.columns:
    raise ValueError(f"Target column '{target_col}' not found. Available columns: {list(df.columns)}")

X = df.drop(columns=[target_col])
y = df[target_col]

# Model and cross-validation
clf = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
y_pred = cross_val_predict(clf, X, y, cv=cv)

# Metrics
acc = accuracy_score(y, y_pred)
prec = precision_score(y, y_pred, average='weighted', zero_division=0)
rec = recall_score(y, y_pred, average='weighted', zero_division=0)
f1 = f1_score(y, y_pred, average='weighted', zero_division=0)
labels = sorted(y.unique())
cm = confusion_matrix(y, y_pred, labels=labels)

# Print metrics table
metrics_table = [
    ["Accuracy", f"{acc:.4f}"],
    ["Precision", f"{prec:.4f}"],
    ["Recall", f"{rec:.4f}"],
    ["F1 Score", f"{f1:.4f}"]
]
print("\nMetrics:")
print(tabulate(metrics_table, headers=["Metric", "Value"], tablefmt="grid"))

# Print confusion matrix
print("\nConfusion Matrix:")
print(tabulate(cm, headers=[f"Pred {c}" for c in labels], showindex=[f"True {c}" for c in labels], tablefmt="grid"))