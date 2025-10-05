# backend API/api.py

from flask import Flask, request, jsonify, send_file
import os
import pandas as pd
import joblib
from werkzeug.utils import secure_filename
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)  # ✅ ENABLE CORS GLOBALLY

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analysis.graphing import plot_histogram, plot_heatmap
from models.modeltrainer import train_supervised_model, load_supervised_model, train_unsupervised_model, load_unsupervised_model
from analysis.reportgenerator import generate_profile_report

UPLOAD_FOLDER = "data/"
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper to check allowed files
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- ROUTES ---

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        return jsonify({"message": "File uploaded successfully", "filename": filename}), 200
    return jsonify({"error": "Invalid file format"}), 400

@app.route("/train-supervised", methods=["POST"])
def train_supervised():
    data = request.get_json()
    df = pd.DataFrame(data["data"])
    X = df.drop(columns=[data["label_column"]])
    y = df[data["label_column"]]
    model = train_supervised_model(X, y)
    return jsonify({"message": "Supervised model trained successfully."})

@app.route("/train-unsupervised", methods=["POST"])
def train_unsupervised():
    data = request.get_json()
    df = pd.DataFrame(data["data"])
    model_type = data.get("model_type", "IsolationForest")  # Default to IsolationForest
    model = train_unsupervised_model(df, model_type)
    return jsonify({"message": f"Unsupervised model ({model_type}) trained successfully."})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    df = pd.DataFrame(data["data"])
    model = load_supervised_model()
    if not model:
        return jsonify({"error": "No trained model found."}), 404
    predictions = model.predict(df)
    return jsonify({"predictions": predictions.tolist()})

@app.route("/profile", methods=["POST"])
def profile_data():
    data = request.get_json()
    df = pd.DataFrame(data["data"])
    report = generate_profile_report(df)
    return jsonify(report)

@app.route("/graph/histogram", methods=["POST"])
def histogram():
    data = request.get_json()
    df = pd.DataFrame(data["data"])
    column = data["column"]
    path = plot_histogram(df, column)
    return send_file(path, mimetype='image/png')

@app.route("/graph/heatmap", methods=["POST"])
def heatmap():
    data = request.get_json()
    df = pd.DataFrame(data["data"])
    path = plot_heatmap(df)
    return send_file(path, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)


