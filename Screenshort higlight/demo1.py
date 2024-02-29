from flask import Flask, render_template, request, send_file
import requests
from bs4 import BeautifulSoup
import pdfkit

app = Flask(__name__)

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

        return soup.prettify()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching content: {e}")
        return None

def convert_to_pdf(html_content, output_file_name):
    try:
        pdfkit.from_string(html_content, output_file_name, options={'quiet': True})

    except Exception as e:
        print(f"Error generating PDF: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        html_content = fetch_content(url)

        if html_content:
            output_file_name = "output.pdf"
            convert_to_pdf(html_content, output_file_name)
            return render_template('result.html', pdf_file=output_file_name)
        else:
            return render_template('error.html')

    return render_template('index.html')

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
