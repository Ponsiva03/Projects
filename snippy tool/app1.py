import io
import os
import time
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
from PIL import Image


@app.route('/snip', methods=['POST'])
def snip():
    canvas_data = request.data

    # Decode the canvas data from base64
    canvas_data_decoded = canvas_data.split(',')[1]
    canvas_data_bytes = bytes(canvas_data_decoded, 'utf-8')

    # Create a PIL Image object from the decoded data
    img = Image.open(io.BytesIO(canvas_data_bytes))

    # Generate a unique filename for the screenshot
    filename = f"screenshot_{int(time.time())}.png"

    # Save the image as a PNG file
    img.save(os.path.join('static', filename))  # Assuming a 'static' folder for storing images

    return f"Screenshot captured and saved as {filename}"  # Return a success message with the filename

if __name__ == "__main__":
    app.run(debug=True)