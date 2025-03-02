from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from .service import process_pdf
import os

quiz_bp = Blueprint('quiz_bp', __name__)

ALLOWED_EXTENSIONS = {'pdf'}
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            return jsonify({"message": "Quiz imported successfully", "data": quiz_data}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            os.remove(file_path)
    else:
        return jsonify({"error": "Invalid file type"}), 400
