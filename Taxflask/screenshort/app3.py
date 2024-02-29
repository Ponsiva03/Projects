import io
from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
from PIL import Image
import urllib3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index3.html')

@app.route("/scrape", methods=["POST"])
def scrape_url():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"})

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch webpage content"})
        
        soup = BeautifulSoup(response.content, "html.parser")
        extracted_content = str(soup.find("your_target_element_selector")).replace('\n', '')
        
        return jsonify({"html": extracted_content})
    
    except Exception as e:
        return jsonify({"error": f"Error: {e}"})

@app.route("/crop", methods=["POST"])
def crop_selection():
    data = request.get_json()
    url = data.get("url")
    iframe_content = data.get("iframeContent")
    left = data.get("left")
    top = data.get("top")
    width = data.get("width")
    height = data.get("height")

    if not all([url, iframe_content, left, top, width, height]):
        return jsonify({"error": "Missing data in request"})

    try:
        content_start_index = iframe_content.find(data["iframeContent"])
        cropped_content = iframe_content[content_start_index + left: content_start_index + left + width]
        cropped_content = cropped_content[:top] + cropped_content[top + height:]

        # Add your image processing logic here...
        # Example:
        # with Image.open("your_image.jpg") as img:
        #     cropped_img = img.crop((left, top, left + width, top + height))
        #     cropped_img.save("cropped_image.jpg")

        # Return a sample response for now
        return jsonify({
            "imageUrl": "/static/cropped_image.jpg",
            "message": "Cropped image saved!"
        })
    
    except Exception as e:
        return jsonify({"error": f"Error: {e}"})

if __name__ == "__main__":
    app.run(debug=True)
