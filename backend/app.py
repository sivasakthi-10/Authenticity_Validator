from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from plagiarism import check_plagiarism
from ai_detector import detect_ai_text

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return jsonify({"message": "Authenticity Validator API Running"})

@app.route('/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"})

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    plagiarism = check_plagiarism(filepath)

    ai_score = detect_ai_text(filepath)

    return jsonify({
        "filename": file.filename,
        "plagiarism_score": plagiarism,
        "ai_generated_score": ai_score,
        "originality": 100-max(plagiarism, ai_score)
    })

if __name__ == "__main__":
    app.run(debug=True)
