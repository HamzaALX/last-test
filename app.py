from flask import Flask, render_template, request, send_file
from pdf2docx import Converter
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pdf_to_word', methods=['GET', 'POST'])
def pdf_to_word():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.pdf'):
            # Save the PDF file
            uploads_dir = 'uploads'
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)
            file_path = os.path.join(uploads_dir, file.filename)
            file.save(file_path)

            # Convert PDF to Word
            downloads_dir = 'downloads'
            if not os.path.exists(downloads_dir):
                os.makedirs(downloads_dir)
            output_path = os.path.join(downloads_dir, file.filename.replace('.pdf', '.docx'))
            cv = Converter(file_path)
            cv.convert(output_path)
            cv.close()

            # Provide the download link
            converted_file = '/' + output_path

            return render_template('pdf_to_word.html', converted_file=converted_file)
        else:
            error = 'Please upload a valid PDF file.'
            return render_template('pdf_to_word.html', error=error)

    return render_template('pdf_to_word.html')

if __name__ == '__main__':
    app.run(debug=True)
