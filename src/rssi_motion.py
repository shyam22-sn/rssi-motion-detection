import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Load dataset
df = pd.read_csv("../data/rssi_features.csv")  # ensure the space in filename if intentional

# Define features and target
X = df[["Mean", "Variance", "StdDev"]]
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define models
models = {
    "SVM": SVC(),
    "kNN": KNeighborsClassifier(),
    "Decision Tree": DecisionTreeClassifier()
}

# Prepare result storage
results = {
    "Model": [],
    "Accuracy": [],
    "Precision": [],
    "Recall": [],
    "F1 Score": []
}

# Train, evaluate, export
for name, model in models.items():
    print(f"\nTraining: {name}")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, pos_label="motion")
    rec = recall_score(y_test, y_pred, pos_label="motion")
    f1 = f1_score(y_test, y_pred, pos_label="motion")
    cm = confusion_matrix(y_test, y_pred)

    print(f"Accuracy: {acc:.4f}")
    print(f"Precision (motion): {prec:.4f}")
    print(f"Recall (motion): {rec:.4f}")
    print(f"F1 Score (motion): {f1:.4f}")
    print("Confusion Matrix:")
    print(cm)

    # Save model
    joblib.dump(model, f"{name.lower().replace(' ', '_')}_model.pkl")

    # Store metrics
    results["Model"].append(name)
    results["Accuracy"].append(acc)
    results["Precision"].append(prec)
    results["Recall"].append(rec)
    results["F1 Score"].append(f1)

# Plot results
results_df = pd.DataFrame(results)
plt.figure(figsize=(10, 6))
results_df.set_index("Model").plot(kind="bar", rot=0)
plt.title("Model Comparison")
plt.ylabel("Score")
plt.ylim(0, 1.1)
plt.grid(True)
plt.tight_layout()
plt.savefig("model_performance_comparison.png")
plt.show()

