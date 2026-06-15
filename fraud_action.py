import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, precision_score
import numpy as npgi
import matplotlib.pyplot as plt

# Load the datasets
file_path1 = r'C:\Users\Taofeek001\Downloads\accounting_dataset.csv'
file_path2 = r'C:\Users\Taofeek001\Downloads\bank_transactions_data_2.csv'
data1 = pd.read_csv(file_path1)
data2 = pd.read_csv(file_path2)

# Combine datasets and fill missing values
data = pd.concat([data1, data2], ignore_index=True)
data.ffill(inplace=True)  # Use forward fill to handle missing values

# Convert categorical variables to numerical
categorical_cols = data.select_dtypes(include=['object']).columns
data = pd.get_dummies(data, columns=categorical_cols, drop_first=True)

# Specify target column (adjust if your dataset uses a different column name)
target_column = 'Risk_Incident'
if target_column not in data.columns:
    raise ValueError(f"Target column '{target_column}' not found in the combined dataset.")

# Separate features and target
X = data.drop(columns=[target_column])
y = data[target_column]

# Check if dataset is empty after preprocessing
if X.empty or y.empty:
    raise ValueError("Feature set or target variable is empty. Check your datasets and preprocessing.")

# Split dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train a Random Forest classifier with balanced class weights
model = RandomForestClassifier(class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Predictions on test data
y_pred = model.predict(X_test)
# Calculate precision score
precision = precision_score(y_test, y_pred, average='macro', zero_division=0.0)


# Evaluation metrics
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print(f"Precision Score: {precision:.4f}")
print(f"Model Accuracy: {model.score(X_test, y_test):.4f}")



# Visualize decision boundary if there are exactly 2 features
if X_train.shape[1] == 2:
    plt.figure(figsize=(8, 6))
    plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, s=30, cmap=plt.cm.Paired, label='Train')
    plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, s=30, marker='x', cmap=plt.cm.Paired, label='Test')
    plt.title('Random Forest Decision Boundary')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.show()
else:
    # If more than 2 features, visualize first two features decision surface with SVM linear kernel
    if X.shape[1] >= 2:
        from sklearn.svm import SVC
        X_vis = X.iloc[:, :2].values
        y_vis = y.values
        X_train_vis, X_test_vis, y_train_vis, y_test_vis = train_test_split(X_vis, y_vis, test_size=0.3, random_state=42)
        scaler_vis = StandardScaler()
        X_train_vis = scaler_vis.fit_transform(X_train_vis)
        X_test_vis = scaler_vis.transform(X_test_vis)
        
        clf = SVC(kernel='linear', random_state=42)
        clf.fit(X_train_vis, y_train_vis)
        
        h = 0.02
        x_min, x_max = X_train_vis[:, 0].min() - 1, X_train_vis[:, 0].max() + 1
        y_min, y_max = X_train_vis[:, 1].min() - 1, X_train_vis[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        
        plt.figure(figsize=(8, 6))
        plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)
        plt.scatter(X_train_vis[:, 0], X_train_vis[:, 1], c=y_train_vis, cmap=plt.cm.cool, edgecolors='k', label='Train')
        plt.xlabel('Feature 1')
        plt.ylabel('Feature 2')
        plt.title('Linear SVM Decision Surface (First Two Features)')
        plt.legend()
        plt.show()
    else:
        print("Not enough features (less than 2) for decision boundary visualization.")
