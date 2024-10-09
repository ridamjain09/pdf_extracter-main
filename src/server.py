from flask import Flask, request, jsonify
from src.chatbot import InsuranceChatbot
from src.exceptions import FileTooLargeException
import os

app = Flask(__name__)
bot = InsuranceChatbot('./data/cleaned_policy.txt')

@app.route('/upload_policy', methods=['POST'])
def upload_policy():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        if file.content_length > 2 * 1024 * 1024:  # 2 MB size limit
            raise FileTooLargeException("File is too large")
        filename = secure_filename(file.filename)
        file.save(os.path.join('./data/raw_pdfs', filename))
        return jsonify({"message": "File uploaded successfully"}), 200
    return jsonify({"error": "Invalid file type"}), 400

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.json.get('question')
    response = bot.ask_question(question)
    return jsonify({"response": response})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

@app.errorhandler(FileTooLargeException)
def handle_file_too_large(e):
    return jsonify({"error": str(e)}), 413

if __name__ == "__main__":
    app.run(debug=True)
