from flask import Flask, render_template, request, flash, redirect, url_for, make_response
import requests
from bs4 import BeautifulSoup
from weasyprint import HTML

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'

@app.route('/', methods=['GET', 'POST'])
def index():
    content = None
    error_message = None

    if request.method == 'POST':
        url = request.form['url']
        content, error_message = get_html_content(url)

        if error_message:
            flash(error_message, 'error')

    return render_template('index4.html', content=content)

def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        pdf_bytes = HTML(string=str(soup)).write_pdf()
        return pdf_bytes, None
    except requests.exceptions.RequestException as e:
        return None, f"Error: {e}"

@app.route('/download_pdf/<url>')
def download_pdf(url):
    content, error_message = get_html_content(url)
    if error_message:
        flash(error_message, 'error')
        return redirect(url_for('index'))

    response = make_response(content)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=web_content.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True)
