import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# ====== LOAD IRIS DATA ======
iris = load_iris()

X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = pd.Series(iris.target)
print(y)
df = pd.DataFrame(iris.data, columns=iris.feature_names)
# ====== PARAMETERS ======
test_size = 0.2
n_estimators = 100
criterion = "gini"
k_folds = 5

# ====== TRAIN-TEST SPLIT ======
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, stratify=y, random_state=42
)

# ====== MODEL ======
rf = RandomForestClassifier(
    n_estimators=n_estimators,
    criterion=criterion,
    random_state=42
)
rf.fit(X_train, y_train)

# ====== CROSS VALIDATION ======
cv = StratifiedKFold(n_splits=k_folds, shuffle=True, random_state=42)

acc_scores = cross_val_score(rf, X_train, y_train, cv=cv, scoring='accuracy')
prec_scores = cross_val_score(rf, X_train, y_train, cv=cv, scoring='precision_macro')
rec_scores = cross_val_score(rf, X_train, y_train, cv=cv, scoring='recall_macro')
f1_scores = cross_val_score(rf, X_train, y_train, cv=cv, scoring='f1_macro')
print("\nCross-Validation Average Scores:")
print(f"Accuracy: {acc_scores.mean():.4f}")
print(f"Precision: {prec_scores.mean():.4f}")
print(f"Recall: {rec_scores.mean():.4f}")
print(f"F1 Score: {f1_scores.mean():.4f}")

# ====== TEST EVALUATION ======
y_pred = rf.predict(X_test)
print("\nTest Set Scores:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred, average='macro'):.4f}")
print(f"Recall: {recall_score(y_test, y_pred, average='macro'):.4f}")
print(f"F1 Score: {f1_score(y_test, y_pred, average='macro'):.4f}")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print(df.head())
