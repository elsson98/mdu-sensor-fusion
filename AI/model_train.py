import pickle

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


data = pd.read_csv('../data-processing/training_data.csv')
data.drop('Spin_ID', axis=1)
data.drop('Cluster', axis=1)
# Splitting the data into input features (X) and target variable (y)
X = data[['Centroid_X', 'Centroid_Y', 'cluster_angle', 'center_x', 'center_y', 'bounding_box_angle']]
y = data['label']

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creating the XGBoost classifier
xgb_classifier = xgb.XGBClassifier()

# Training the model
xgb_classifier.fit(X_train, y_train)

model_file = 'xgb_model.pkl'
pickle.dump(xgb_classifier, open(model_file, 'wb'))

# Making predictions on the test set
y_pred = xgb_classifier.predict(X_test)

# Evaluating the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
