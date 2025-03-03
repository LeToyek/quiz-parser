from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from .utils import process_pdf
from .service import parse_pdf
import os
import json

quiz_bp = Blueprint('quiz_bp', __name__)

ALLOWED_EXTENSIONS = {'pdf','png','jpg','jpeg'}
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@quiz_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"message": "Quiz service is healthy"}), 200

@quiz_bp.route('/import-quiz', methods=['POST'])
def import_quiz():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        try:
            quiz_data = process_pdf(file_path)
            joined_data = "\n".join(quiz_data)
            # return jsonify({"message": "Quiz imported successfully", "data": joined_data}), 200
            content = parse_pdf(joined_data)
            parsed_data = json.loads(content)
            return jsonify({"message": "Quiz imported successfully", "data": parsed_data}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            os.remove(file_path)
    else:
        return jsonify({"error": "Invalid file type"}), 400
