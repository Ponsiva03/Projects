from flask import Flask, render_template, request, jsonify
from PIL import Image
from io import BytesIO
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/crop', methods=['POST'])
def crop_image():
    # Get coordinates from frontend
    crop_data = request.get_json()
    x1, y1, x2, y2 = int(crop_data['x1']), int(crop_data['y1']), int(crop_data['x2']), int(crop_data['y2'])

    # Get iframe screenshot
    response = requests.get("https://example.com")  # Replace with your iframe URL
    img = Image.open(BytesIO(response.content))

    # Crop the image
    cropped_img = img.crop((x1, y1, x2, y2))

    # Save or process the cropped image
    # For example, save the cropped image to a file
    cropped_img.save("cropped_image.png")

    return jsonify({'message': 'Image cropped successfully'})

if __name__ == '__main__':
    app.run(debug=True)
