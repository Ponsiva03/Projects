import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import ImageGrab
from fpdf import FPDF

# Get user input for URL
url = input("Enter the web page URL: ")

# Open the web page
browser = webdriver.Chrome()  # Replace with your preferred browser driver
browser.get(url)

# Function to capture a cropped image
def capture_cropped_image():
    x1, y1, x2, y2 = map(int, input("Enter crop coordinates (x1, y1, x2, y2): ").split())
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    filename = f"crop_{x1}_{y1}_{x2}_{y2}.png"
    img.save(filename)
    return filename

# Create a PDF object
pdf = FPDF()

# Capture and save cropped images repeatedly until user chooses to stop
while True:
    filename = capture_cropped_image()
    pdf.add_page()
    pdf.image(filename, x=0, y=0, w=210, h=297)  # Adjust width and height as needed

    choice = input("Capture another image? (y/n): ")
    if choice.lower() != 'y':
        break

# Save the PDF
pdf.output("cropped_images.pdf", "F")

# Close the browser
browser.quit()
