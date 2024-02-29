import webbrowser
from flask import Flask, render_template, request, jsonify
import pyautogui
import datetime
import os
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load_webpage', methods=['POST'])
def load_webpage():
    data = request.get_json()
    url = data.get('url')
    
    webbrowser.open(url)

    return jsonify({'message': 'Webpage loaded'})

@app.route('/take_screenshot', methods=['POST'])
def take_screenshot():
    data = request.get_json()
    x1 = data.get('x1')
    y1 = data.get('y1')
    x2 = data.get('x2')
    y2 = data.get('y2')

    image = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    file_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")

    directory = 'snips'
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, file_name + ".png")
    image.save(file_path)
    return jsonify({'file_path': file_path})

@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.get_json()
    sku = data.get('sku')
    url = data.get('url')
    screenshot_path = data.get('screenshot_path')

    filename = "screenshot_data.csv"
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([sku, url, screenshot_path])

    return jsonify({'message': 'Data saved successfully'})

if __name__ == '__main__':
    app.run(debug=True)
