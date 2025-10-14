from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
from PyPDF2 import PdfReader

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Grouped skills for analysis
SKILL_CATEGORIES = {
    "Programming Languages": ["python", "java", "c++", "javascript", "typescript", "go", "c#", "ruby"],
    "Web Development": ["react", "flask", "django", "express", "html", "css", "node", "angular", "vue"],
    "Databases": ["sql", "mysql", "mongodb", "postgresql", "redis"],
    "DevOps & Cloud": ["docker", "kubernetes", "aws", "azure", "ci/cd", "nginx", "jenkins"],
    "Tools & Platforms": ["git", "github", "vscode", "postman", "linux", "jira"],
    "AI / ML": ["tensorflow", "scikit-learn", "pytorch", "nlp", "pandas", "numpy"]
}

# Expanded synonyms / variations
SYNONYMS = {
    "javascript": ["js", "java script"],
    "aws": ["amazon web services"],
    "node": ["node.js", "nodejs"],
    "c#": ["c sharp"],
    "ci/cd": ["ci cd", "continuous integration", "continuous deployment"],
    "html": ["hypertext markup language"],
    "css": ["cascading style sheets"],
    "flask": ["flask framework"],
    "django": ["django framework"],
    "react": ["react.js", "reactjs"],
    "python": ["py"]
}

def clean_text(text):
    """Clean PDF text: remove extra spaces, weird chars, normalize common ligatures."""
    text = text.replace("\ufb01", "fi")  # fix ligature
    text = re.sub(r'[\n\r]+', ' ', text)  # replace newlines with space
    text = re.sub(r'\s+', ' ', text)      # remove multiple spaces
    text = re.sub(r'[•–—]', ' ', text)    # replace bullets/dashes
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # remove non-ASCII characters
    return text.lower().strip()

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        reader = PdfReader(filepath)
        extracted_text = ""

        for page in reader.pages:
            extracted_text += page.extract_text() or ""

        cleaned_text = clean_text(extracted_text)

        if not cleaned_text:
            return jsonify({"error": "Unable to extract text from PDF"}), 500

        # Grouped skill matching with synonyms
        category_matches = {}
        category_missing = {}
        total_skills = 0
        matched_skills_count = 0

        for category, skills in SKILL_CATEGORIES.items():
            matched = []
            for skill in skills:
                # check main skill
                if skill in cleaned_text:
                    matched.append(skill)
                # check synonyms
                elif skill in SYNONYMS:
                    for syn in SYNONYMS[skill]:
                        if syn in cleaned_text:
                            matched.append(skill)
                            break
            missing = [skill for skill in skills if skill not in matched]
            
            category_matches[category] = matched
            category_missing[category] = missing

            total_skills += len(skills)
            matched_skills_count += len(matched)

        score = round((matched_skills_count / total_skills) * 100, 2)

        return jsonify({
            "skill_match_score": score,
            "matched_by_category": category_matches,
            "missing_by_category": category_missing,
            "preview": extracted_text[:400]  # optional preview
        })

    except Exception as e:
        return jsonify({"error": f"Failed to read PDF: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
