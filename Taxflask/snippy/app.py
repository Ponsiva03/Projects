import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import io
import requests
from bs4 import BeautifulSoup

def save_csv(sku, url, path):
    with open('output.csv', mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([sku, url, path])

def get_screenshot(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    screenshot = driver.get_screenshot_as_png()
    driver.quit()
    return screenshot

def crop_image(screenshot, crop_area):
    img = Image.open(io.BytesIO(screenshot))
    top, left, bottom, right = crop_area
    img_cropped = img.crop((left, top, right, bottom))
    return img_cropped

def main():
    url = input("Enter the web URL: ")
    sku = input("Enter the SKU label: ")

    # You need to specify the crop area (top, left, bottom, right) according to your web page structure
    crop_area = (500, 500, 500, 500)

    # Get the screenshot
    screenshot = get_screenshot(url)

    # Crop the image
    img_cropped = crop_image(screenshot, crop_area)

    # Save the cropped image as a PNG file
    img_cropped.save('output.png')

    # Save SKU, URL, and path in csv file
    save_csv(sku, url, 'output.png')

if __name__ == "__main__":
    main()