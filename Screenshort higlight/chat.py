from flask import Flask, render_template, request, jsonify, send_file
import fitz
import pdfkit
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert_highlight', methods=['POST'])
def convert_and_highlight():
    html_link = request.form.get('html_link')
    selected_word = request.form.get('word')

    # Download HTML content from the provided link
    html_content = download_html(html_link)

    # Convert HTML to PDF
    pdf_path = 'output.pdf'
    convert_html_to_pdf(html_content, pdf_path)

    # Highlight the selected word in the PDF
    highlight_word(pdf_path, selected_word)

    # Provide a message to the user
    message = f"Conversion and highlighting done! Selected word: {selected_word}"
    
    # Return the result as JSON to be handled by the frontend
    return jsonify({'message': message, 'pdf_path': 'highlighted_output.pdf'})

def download_html(html_link):
    response = requests.get(html_link)
    return response.text

def convert_html_to_pdf(html_content, output_path):
    pdfkit.from_file(html_content, output_path)

def highlight_word(pdf_path, word):
    doc = fitz.open(pdf_path)
    page = doc[0]  # Assuming you want to highlight on the first page

    # Search for the word and get its coordinates
    rect = page.search_for(word)

    # Highlight the word
    page.add_highlight_annot(rect)

    # Save the modified PDF
    highlighted_path = 'highlighted_output.pdf'
    doc.save(highlighted_path)
    doc.close()

    return highlighted_path

if __name__ == '__main__':
    app.run(debug=True)
