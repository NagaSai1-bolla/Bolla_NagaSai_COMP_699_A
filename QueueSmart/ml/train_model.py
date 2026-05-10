import numpy as np
from sklearn.linear_model import LinearRegression
import pickle
import os


def train_model():
    # ==========================
    # GENERATE SYNTHETIC DATA
    # ==========================
    np.random.seed(42)

    queue_length = np.random.randint(1, 20, 100)
    avg_service_time = np.random.randint(2, 10, 100)

    # Target (waiting time)
    waiting_time = queue_length * 2 + avg_service_time * 1.5

    X = np.column_stack((queue_length, avg_service_time))
    y = waiting_time

    # ==========================
    # TRAIN MODEL
    # ==========================
    model = LinearRegression()
    model.fit(X, y)

    # ==========================
    # SAVE MODEL
    # ==========================
    os.makedirs("ml", exist_ok=True)

    with open("ml/model.pkl", "wb") as f:
        pickle.dump(model, f)

    print(" Model trained and saved successfully")