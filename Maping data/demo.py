from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Store the used URLs in a set
used_urls = set()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        if url not in used_urls:
            used_urls.add(url)
            # Send a GET request to the URL and get the response content
            response = requests.get(url)
            content = response.content
            # Check if the web page is displayed within an iframe
            soup = BeautifulSoup(content, 'html.parser')
            iframe = soup.find('iframe')
            if iframe:
                iframe_src = iframe.get('src')
                if iframe_src:
                    # Display the iframe content
                    iframe_content = f'<iframe sandbox="allow-same-origin" src="{iframe_src}"></iframe>'
                    return render_template_string(iframe_content)
            else:
                # Scrape the data from the web page
                soup = BeautifulSoup(content, 'html.parser')
                # Extract the data you need (e.g., text, links, etc.)
                data = soup.get_text()
                return f'Data from {url}:\n{data}'
        else:
            return 'This URL has already been used.'
    else:
        return render_template_string('''
            <form method="post">
                <input type="text" name="url">
                <input type="submit" value="Submit">
            </form>
        ''')

if __name__ == '__main__':
    app.run()