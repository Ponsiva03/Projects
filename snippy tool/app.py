from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load_url', methods=['POST'])
def load_url():
    sku = request.form['sku']
    web_url = request.form['web_url']
    return render_template('index.html', sku=sku, web_url=web_url)

if __name__ == "__main__":
    app.run(debug=True)  
