import pickle
from google.cloud import storage
from flask import Flask, request, jsonify


# Basic Flask app to serve predictions
app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    html = "healthy"
    return html.format(format)

@app.route('/predict', methods=['POST'])
def predict():
    # Get input records
    payload = request.json
    instances = payload.get('instances', [])
    
    # Set placeholder for predictions
    predictions = []

    # Loop through instances
    for instance in instances:
        prediction = model.predict(instance)
        predictions.append(prediction[0])

    # Return predictions
    return jsonify({'predictions': predictions})

if __name__ == '__main__':
    # Download pre-trained Random Forest model from GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket("simple-pipeline-415719-bucket")
    blob = bucket.blob('model.pkl')
    blob.download_to_filename('model.pkl')

    # Load model
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    print("Model loaded")

    # Start Flask app
    app.run(debug=True, host='0.0.0.0', port=8080)