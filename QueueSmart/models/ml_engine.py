import pickle
import os


class WaitingTimeMLEngine:

    MODEL_PATH = "ml/model.pkl"

    @staticmethod
    def load_model():
        if not os.path.exists(WaitingTimeMLEngine.MODEL_PATH):
            return None

        with open(WaitingTimeMLEngine.MODEL_PATH, "rb") as f:
            return pickle.load(f)

    @staticmethod
    def predict(queue_length, avg_service_time):
        model = WaitingTimeMLEngine.load_model()

        # If model not trained yet → fallback formula
        if model is None:
            return int(queue_length * 2 + avg_service_time * 1.5)

        # ML prediction
        prediction = model.predict([[queue_length, avg_service_time]])

        return int(prediction[0])