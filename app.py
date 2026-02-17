from flask import Flask, request, jsonify
import os
from data_processing.analyze import analyze_data

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Analyze only — visualization now in Streamlit
    insights = analyze_data(filepath)

    return jsonify({'insights': insights, 'filename': file.filename})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
