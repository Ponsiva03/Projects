from flask import Flask, render_template, request, flash, redirect, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SECRET_KEY'] = '12344'

@app.route('/', methods=['GET', 'POST'])
def index():
    content = None
    error_message = None

    if request.method == 'POST':
        url = request.form['url']
        content, error_message = get_html_content(url)

        if error_message:
            flash(error_message, 'error')

    return render_template('index_modified.html', content=content)

def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        content = str(soup)
        return content, None
    except requests.exceptions.RequestException as e:
        return None, f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
