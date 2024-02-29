import os
import pdfkit
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, flash, send_from_directory
from weasyprint import HTML

app = Flask(__name__)
app.secret_key = '1234'

# Define a constant for the upload directory
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def fetch_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove unwanted elements or apply CSS styling (optional)
        if True:  # Replace with your filtering/styling logic
            for script in soup.find_all('script'):
                script.decompose()  # Remove scripts
            for style in soup.find_all('style'):
                style.decompose()  # Remove inline styles

        return soup.prettify()  # Indented HTML for better readability

    except requests.exceptions.RequestException as e:
        flash(f"Error fetching content: {e}")
        return None

def convert_to_pdf(html_content, output_file_name):
    try:
        pdfkit.from_string(html_content, output_file_name, options={'quiet': True})
    except Exception as e:
        flash(f"Error generating PDF: {e}")

def sanitize_filename(filename):
    # Replace invalid characters in the filename
    return ''.join(c if c.isalnum() or c in ['.', '_'] else '_' for c in filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    pdf_url = None  # Initialize pdf_url variable

    if request.method == 'POST':
        url = request.form['url']
        html_content = fetch_content(url)

        if html_content:
            output_file_name = sanitize_filename(url.split('/')[-1] + ".pdf")
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], output_file_name)

            convert_to_pdf(html_content, pdf_path)

            # Set pdf_url to be used in the template
            pdf_url = output_file_name  # Use the filename, not the full path

        else:
            flash("Error fetching content.")

    return render_template('index5.html', pdf_url=pdf_url)

# Serve PDFs from the UPLOAD_FOLDER
@app.route('/uploads/<filename>')
def serve_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    # Create the UPLOAD_FOLDER if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True)




# ----------------------------------------------------------------------------working-----------------------------------------------------------------------------------------------------