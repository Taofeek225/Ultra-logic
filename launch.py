from flask import Flask, request, jsonify
import logging
import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np

app = Flask(__name__)

# Setup logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Initialize a simple in-memory model and scaler for demonstration
model = RandomForestClassifier(class_weight='balanced')
scaler = StandardScaler()
is_trained = False

# Initialize SQLite database connection and create table
def init_db():
    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_data TEXT,
            prediction INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/train', methods=['POST'])
def train():
    """
    Expects JSON body with 'data' containing list of dicts with features and 'target' list
    Example:
    {
      "data": [ {"feature1":1, "feature2":2}, ... ],
      "target": [0, 1, 0, ...]
    }
    """
    global model, scaler, is_trained
    try:
        req = request.get_json()
        df = pd.DataFrame(req['data'])
        y = np.array(req['target'])
        # Scale features
        X_scaled = scaler.fit_transform(df)
        model.fit(X_scaled, y)
        is_trained = True
        logging.info("Model trained successfully.")
        return jsonify({"message": "Model trained successfully."}), 200
    except Exception as e:
        logging.error(f"Training failed: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/predict', methods=['POST'])
def predict():
    """
    Expects JSON body with single transaction features:
    {
      "data": {"feature1": value, "feature2": value, ...}
    }
    Returns prediction and stores it in DB.
    """
    global is_trained
    if not is_trained:
        return jsonify({"error": "Model is not trained yet."}), 400
    try:
        req = request.get_json()
        input_df = pd.DataFrame([req['data']])
        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)[0]
        # Store in DB
        conn = sqlite3.connect('predictions.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO predictions (input_data, prediction) VALUES (?, ?)',
                       (str(req['data']), int(prediction)))
        conn.commit()
        conn.close()
        logging.info(f"Prediction made: {prediction} for input {req['data']}")
        return jsonify({"prediction": int(prediction)})
    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
