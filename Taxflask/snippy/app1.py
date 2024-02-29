from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pywebio.input import *
from pywebio.output import *
from PIL import Image
import time

from app import main

options = Options()
options.headless = True  # Comment this line for visible browser
driver = webdriver.Chrome(options=options)

url = input("Enter the web page URL: ")
driver.get(url)

# Inject JavaScript code for drag-and-select functionality
# Inject JavaScript code for drag-and-select functionality
driver.execute_script("""
// JavaScript code to create a draggable rectangle for selection
const rect = document.createElement('div');
rect.style.position = 'absolute';
rect.style.border = '1px solid black';
rect.style.opacity = 0.5;
document.body.appendChild(rect);

let isDragging = false;
let startX, startY;

document.addEventListener('mousedown', (event) => {
    startX = event.clientX;
    startY = event.clientY;
    rect.style.width = '0px';
    rect.style.height = '0px';
    rect.style.left = startX + 'px';
    rect.style.top = startY + 'px';
    isDragging = true;
});

document.addEventListener('mousemove', (event) => {
    if (isDragging) {
        rect.style.width = (event.clientX - startX) + 'px';
        rect.style.height = (event.clientY - startY) + 'px';
    }
});

document.addEventListener('mouseup', (event) => {
    isDragging = false;
    const cropArea = {
        x: startX,
        y: startY,
        width: event.clientX - startX,
        height: event.clientY - startY
    };
    // Pass cropArea back to Python using execute_script()
    // ...
});
""")

# Wait for user selection and receive coordinates
while True:
    crop_area = driver.execute_script("return window.cropArea")
    if crop_area:
        break
    time.sleep(0.1)  # Check for coordinates every 0.1 seconds

screenshot = driver.get_screenshot_as_png()
driver.quit()

# Crop and save the image using Pillow
img = Image.open(screenshot)
cropped_img = img.crop(crop_area)
cropped_img.save("cropped_content.png")

# Display the cropped image using PyWebIO
put_image("cropped_content.png", width=600)


if __name__ == "__main__":
    main()
