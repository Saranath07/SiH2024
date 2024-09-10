from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
import time
# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# Dummy Aadhar Data for matching
DUMMY_AADHAR_DATA = {
    "name": "R Srimathi",
    "dob": "2004-04-02",
    "gender": "Female",
    "aadharNumber": "123456789012"
}

@app.route('/upload', methods=['POST'])
def upload_document():
    if 'document' not in request.files:
        return jsonify({"error": "No document uploaded"}), 400

    document = request.files['document']

    #use ur ML MODEL to to overwrite the dummy aadhar data
    if document:
        # Returning dummy data for the uploaded document
        time.sleep(5)
        return jsonify(DUMMY_AADHAR_DATA), 200
        
    else:
        return jsonify({"error": "File upload failed"}), 400
    


DUMMY_PAN_DATA = {
    "name": "R Srimathi",
    "fathersName": "V Renga",
    "dob": "2004-04-02",
    "panNumber": "ABCDE1234F"
}

@app.route('/panupload', methods=['POST'])
def pan_upload_document():
    if 'document' not in request.files:
        return jsonify({"error": "No document uploaded"}), 400

    document = request.files['document']
    
    
    # Just checking if the document was received (no saving)
    if document:
        # Returning dummy data for the uploaded PAN card
        time.sleep(5)
        return jsonify(DUMMY_PAN_DATA), 200
    else:
        return jsonify({"error": "File upload failed"}), 400
@app.route('/')
def index():
    return "Welcome to the Flask App!"

if __name__ == '__main__':
    app.run(debug=True)