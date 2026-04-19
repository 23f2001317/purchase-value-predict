import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
import os

# Create dummy train data
X_train = np.array([[25, 30000], [35, 50000], [45, 80000], [20, 20000], [55, 120000]])
# Purchase value
y_train = np.array([100, 250, 400, 50, 600])

model = LinearRegression()
model.fit(X_train, y_train)

# Ensure backend directory exists
os.makedirs("backend", exist_ok=True)

with open("backend/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Dummy model saved to backend/model.pkl")
