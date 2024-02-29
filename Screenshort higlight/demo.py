from flask import Flask, render_template, request, jsonify
import fitz  # PyMuPDF library for PDF manipulation

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']

        if pdf_file and pdf_file.filename.endswith('.pdf'):
            temp_path = 'static/temp.pdf'
            pdf_file.save(temp_path)

            # Extract text from the PDF and store it in the session
            doc = fitz.open(temp_path)
            text = ''
            for page in doc:
                text += page.get_text()
            request.session['pdf_text'] = text

            return render_template('index1.html', pdf_path='/static/temp.pdf')

    return render_template('index1.html')

@app.route('/highlight', methods=['POST'])
def highlight():
    word = request.form['word']
    pdf_path = request.form['pdf_path']

    # Load the PDF text from the session and find the word
    pdf_text = request.session.pop('pdf_text', '')
    if not pdf_text:
        return jsonify({'error': 'PDF text not found'})
    start_index = pdf_text.find(word)
    if start_index == -1:
        return jsonify({'error': 'Word not found in PDF'})

    # Add a pink rectangle annotation to the PDF
    doc = fitz.open(pdf_path)
    page = doc[0]
    rect = fitz.Rect(page.bbox[0] + 10, page.bbox[1] + 10,
                     page.bbox[0] + 10 + page.text_size(word, fontname='DejaVuSans'),
                     page.bbox[1] + 10 + page.text_size(word, fontname='DejaVuSans', height=20))
    annot = page.add_redaction_annot(rect)
    annot.set_redaction_color(0, 128, 128)
    annot.set_redaction_color(255, 0, 0)
    annot.update()
    doc.save(pdf_path)

    # Return the updated PDF path and the word coordinates
    page_index = 0
    x0, y0, x1, y1 = rect.left, rect.bottom, rect.right, rect.top
    return jsonify({'pdf_path': pdf_path, 'word': word, 'page_index': page_index, 'coordinates': [x0, y0, x1, y1]})

if __name__ == '__main__':
    app.run(debug=True)