from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from PyPDF2 import PdfReader

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # ✅ Extract text from PDF
    try:
        reader = PdfReader(filepath)
        extracted_text = ""

        for page in reader.pages:
            extracted_text += page.extract_text() or ""

        if not extracted_text.strip():
            return jsonify({"error": "Unable to extract text from PDF"}), 500

        # ✅ Define skills we want to check for
        TARGET_KEYWORDS = [
            "python", "flask", "react", "javascript", "node", "sql", 
            "html", "css", "docker", "aws"
        ]

        text_lower = extracted_text.lower()
        matched_keywords = [kw for kw in TARGET_KEYWORDS if kw in text_lower]
        missing_keywords = [kw for kw in TARGET_KEYWORDS if kw not in matched_keywords]

        score = round((len(matched_keywords) / len(TARGET_KEYWORDS)) * 100, 2)

        return jsonify({
            "skill_match_score": score,
            "matched": matched_keywords,
            "missing": missing_keywords,
            "preview": extracted_text[:400]  # optional preview
        })

    except Exception as e:
        return jsonify({"error": f"Failed to read PDF: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
