# Import the necessary libraries
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Assume you have a dataframe `df` with 6 input features and a binary target feature
# For the sake of this example, let's create a dummy dataframe

np.random.seed(0)

num_samples = 1000
num_features = 6
X = np.random.rand(num_samples, num_features)
y = np.random.randint(2, size=num_samples)

df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(num_features)])
df['target'] = y

# Split the dataframe into input features (X) and target feature (y)
X = df.drop('target', axis=1)
y = df['target']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize XGBoost's classifier
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss')

# Fit the classifier with the training data
xgb.fit(X_train, y_train)

# Predict the target values for the test data
y_pred = xgb.predict(X_test)

# Calculate the accuracy of the predictions
accuracy = accuracy_score(y_test, y_pred)

print(f'Accuracy: {accuracy * 100:.2f}%')