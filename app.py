from flask import Flask, render_template, request
from summarizer.extractive import extractive_summary_nlp
import os
import PyPDF2  # pip install PyPDF2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_file(file_path):
    ext = file_path.rsplit('.', 1)[1].lower()
    if ext == 'txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    elif ext == 'pdf':
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + " "
        return text
    return ""

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    user_text = ""

    if request.method == "POST":
        file = request.files.get('file_upload')
        if file and allowed_file(file.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            try:
                user_text = read_file(file_path)
            except Exception as e:
                summary = f"Error reading file: {e}"
                user_text = ""
        else:
            user_text = request.form.get("user_text", "").strip()

        if not user_text:
            summary = "Please enter some text or upload a file."
        else:
            summary = extractive_summary_nlp(user_text)

    return render_template("index.html", summary=summary, user_text=user_text)

if __name__ == "__main__":
    app.run(debug=True)
