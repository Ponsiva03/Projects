from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/load_url', methods=['POST'])
def load_url():
    url = request.form['url']
    page_content = get_page_content(url)
    return page_content

def get_page_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return str(soup)
    except Exception as e:
        return f"Error: {e}"


@app.route('/take_screenshot', methods=['POST'])
def take_screenshot():
    try:
        url = request.form['url']

        # Set up Selenium WebDriver (Make sure you have the appropriate WebDriver for your browser installed)
        driver = webdriver.Chrome()  # You can use Chrome or other browsers supported by Selenium
        driver.get(url)
        
        # Take multiple screenshots
        num_of_screenshots = 5  # Change this to the desired number of screenshots
        screenshots_dir = 'screenshots'
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        for i in range(num_of_screenshots):
            time.sleep(2)  # Adjust this delay according to your needs
            screenshot_path = os.path.join(screenshots_dir, f"screenshot_{i+1}.png")
            driver.save_screenshot(screenshot_path)

        driver.quit()  # Close the browser after taking screenshots
        return "Screenshots captured successfully!"
    except Exception as e:
        return f"Error capturing screenshots: {e}"

if __name__ == '__main__':
    app.run(debug=True)
