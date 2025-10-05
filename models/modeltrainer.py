
import os
import joblib
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.cluster import KMeans

MODEL_PATH = "models/supervised_model.pkl"
UNSUPERVISED_MODEL_PATH = "models/unsupervised_model.pkl"

def train_supervised_model(X, y, allow_partial=True):
    os.makedirs("models", exist_ok=True)

    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("[INFO] Loaded existing model.")
        if not allow_partial:
            return model
    else:
        model = SGDClassifier(random_state=42)
        print("[INFO] Initialized new model.")

    if not hasattr(model, "classes_"):
        model.partial_fit(X, y, classes=np.unique(y))
    else:
        model.partial_fit(X, y)

    joblib.dump(model, MODEL_PATH)
    print("[INFO] Saved model to:", MODEL_PATH)
    return model

def load_supervised_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

def train_unsupervised_model(data, model_type='KMeans'):
    if model_type == 'KMeans':
        model = KMeans(n_clusters=3, random_state=42)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
    
    model.fit(data)
    joblib.dump(model, UNSUPERVISED_MODEL_PATH)
    print("[INFO] Saved unsupervised model to:", UNSUPERVISED_MODEL_PATH)
    return model

def load_unsupervised_model():
    if os.path.exists(UNSUPERVISED_MODEL_PATH):
        return joblib.load(UNSUPERVISED_MODEL_PATH)
    return None