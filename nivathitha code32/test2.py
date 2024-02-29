#import
from flask import Flask,request, render_template, current_app, send_file, jsonify
from fileinput import filename
import pandas as pd
import numpy as np
import os
pd.options.mode.chained_assignment = None
import requests
import json
from urllib.request import urlopen , Request
from bs4 import BeautifulSoup
#import openai 
import PyPDF2
from PyPDF2 import PdfReader 
import io
import google.generativeai as genai
from colorama import Fore
import time
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pdfkit 
import requests
def capture_html_page(url, sku_id):
    folder_name = 'PNGFolder'
    os.makedirs(folder_name, exist_ok=True)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    body_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(driver.get_window_size()['width'], scroll_height)
    try:
        full_page_screenshot = driver.get_screenshot_as_png()
        with open(os.path.join(folder_name, f"{sku_id}.png"), "wb") as f:
            f.write(full_page_screenshot)
        print(f"Full-page screenshot captured and saved as {folder_name}/{sku_id}.png.")
    except Exception as e:
        print(f"Error capturing HTML page screenshot: {e}")
    driver.quit()

# capture pdf pages
def capture_pdf_page(pdf_link,page_index, sku_id):
    folder_name = 'PDFFolder'
    os.makedirs(folder_name, exist_ok=True)
    response = requests.get(pdf_link)
    with open(os.path.join(folder_name, f'{sku_id}_page{page_index}.pdf'), 'wb') as output_file:
        writer = PyPDF2.PdfWriter()
        reader = PyPDF2.PdfReader(io.BytesIO(response.content))
        try:
            page = reader.pages[page_index]
            writer.add_page(page)
            writer.write(output_file)
            print(f"PDF page {page_index} captured and saved as {folder_name}/{sku_id}_page{page_index}.pdf.")
        except IndexError:
            print("Invalid PDF page index.")

def fetch_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove unwanted elements or apply CSS styling (optional)
        if True:  # Replace with your filtering/styling logic
            for script in soup.find_all('script'):
                script.decompose()  # Remove scripts
            for style in soup.find_all('style'):
                style.decompose()  # Remove inline styles

        return soup.prettify()  # Indented HTML for better readability

    except requests.exceptions.RequestException as e:
        print(f"Error fetching content: {e}")
        return None
def convert_to_pdf(html_content, output_file_name):
    try:
        # Use WeasyPrint for better quality and handling of complex HTML
        pdfkit.from_string(html_content, output_file_name, options={'quiet': True})

    except Exception as e:
        print(f"Error generating PDF: {e}")
# Reading master file and columns
print(os.linesep)
print(Fore.YELLOW + '*****************************')
input_file = input(Fore.WHITE + "Please enter input file with extension (.xlsx): ")
df = pd.read_excel('files/' + input_file)
df_tax = pd.read_excel('files/attr_name.xlsx')
df = df.fillna('')
url_cols = [col for col in df.columns if 'URL' in col]
page_cols = [col for col in df.columns if 'PAGE' in col]

# gemini api related settings
os.environ['GOOGLE_API_KEY'] = "AIzaSyBly__5cbui-qyre-b-Cmgg4j6_fnu2beQ"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

generation_config = {
    "temperature": 0,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    # ... (safety settings remain the same)
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

question = 'from the given context fetch the actual attribute name, referred attribute name, attribute values, and unit of measurement (UOM) '

# within the file operations and generate resultant data
print(len(df))
for i in range(0, len(df)):
    sku_for_excel = []
    mpn_for_excel = []
    node = []
    attr = []
    url_data_for_excel = []
    url_data = []
    page_data = []
    pdf_data = []
    res_data = []
    missing_attributes = {}
    node.append(df['END NODE'][i])

    for m in range(0, len(df_tax)):
        if df_tax['End Node'][m] == df['END NODE'][i]:
            attr.append(df_tax['Attribute'][m])

    for j in range(0, len(url_cols)):
        if df[url_cols[j]][i] != '':
            sku_for_excel.append(df['SKU_ID'][i])
            mpn_for_excel.append(df['MPN'][i])
            url_data_for_excel.append(df[url_cols[j]][i])
            url_data.append(df[url_cols[j]][i])
            if '.pdf' in df[url_cols[j]][i]:
                page_data.append(math.floor(df[page_cols[j]][i]))
            else:
                page_data.append('')

    for k in range(0, len(url_data)):
        if '.pdf' in url_data[k]:
            print(url_data[k])
            url = url_data[k]
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Windows; Windows x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'}
            response = requests.get(url=url, headers=headers, timeout=120)
            on_fly_mem_obj = io.BytesIO(response.content)
            pdf_file = PdfReader(on_fly_mem_obj)
            page_num_list = str(page_data[k]).split(',')
            text = []
            for p in range(0, len(page_num_list)):
                page = pdf_file.pages[int(float(page_num_list[p])) - 1]
                # capture_pdf_page(url_data[k],int(float(page_num_list[p]))-1,df['SKU_ID'][i])
                text.append(page.extract_text())
            text = ','.join(text)

            prompt_parts = [
                "Here is the context" + text,
                "Those are the actual Attribute Names" + ','.join(attr),
                question,
                "Return the result in row, column format. Row separator should be '~' and column separator should be '>'. Each row should contain 4 values, in case of blank value return NA "
            ]

            response = model.generate_content(prompt_parts)
            res_data.append(response.text)

        else:
            url = url_data[k]
            # capture_html_page(url_data[k],df['SKU_ID'][i])
            req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(req).read()
            soup = BeautifulSoup(html, features="html.parser")
            header = soup.find('header')
            if header:
                header.decompose()
            footer = soup.find('footer')
            if footer:
                footer.decompose()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            prompt_parts = [
                "Here is the context" + text,
                "Those are the actual Attribute Names" + ','.join(attr),
                question,
                "Return the result in tabular format where Row separator should be '~' and column separator should be '>'. Each row should contain 4 values, in case of blank value return NA "
            ]

            response = model.generate_content(prompt_parts)
            res_data.append(response.text)

    for l in range(0, len(res_data)):
        df1 = pd.read_csv('all_data.csv')
        response_text_list = list(res_data[l].split('\n'))
        sku_id = str(sku_for_excel[l])
        mpn_data = str(mpn_for_excel[l])
        url_data = str(url_data_for_excel[l])
        print(url_data_for_excel[l])

        # Ensure that missing_attributes is defined
        if missing_attributes:
            for missing_attr, missing_value in missing_attributes.items():
                if missing_value == 'NA':
                    for other_res_data in res_data:
                        if missing_attr in other_res_data:
                            missing_value = other_res_data[missing_attr]
                            break

        if '.pdf' in url:
            response = requests.get(url_data_for_excel[l])
            file = open("static/" + str(sku_for_excel[l]) + '_' + str(l) + '.pdf', "wb")
            print(response.content)
            file.write(response.content)
            file.close()
        else:
            print(fetch_content)
            html_content = fetch_content(url_data_for_excel[l])
            output_file_name = str(sku_for_excel[l]) + '_' + str(l) + '.pdf'
            convert_to_pdf(html_content, "static/" + output_file_name)

        local_url = "file:///C:/python files/nivathitha code/static" + str(sku_for_excel[l]) + '_' + str(l) + '.pdf'
        attr_data = response_text_list
        df_data = [[sku_id, mpn_data, url_data, local_url, attr_data]]
        df2 = pd.DataFrame(df_data, columns=['SKU ID', 'MPN', 'URL', 'LOCAL URL', 'ATTR'])
        df3 = pd.concat([df1, df2], ignore_index=True)
        df3 = df3.explode('ATTR')
        # df3.loc[df3['SKU ID'] == sku_id, missing_attr] = missing_value
        df3 = df3[df3["ATTR"].str.contains("Attribute") == False]
        # df3.loc[df3['SKU ID'] == sku_id, missing_attr] = missing_value
        df3.to_csv('all_data.csv', index=False)
    df4 = pd.read_csv('all_data.csv')
    df4[['Original ATTR Name', 'Refered ATTR Name', 'ATTR Value', 'UOM']] = df4['ATTR'].str.split('>', n=3, expand=True)
    df4 = df4.drop('ATTR', axis=1)
    df4.to_csv('final.csv', index=False)
    print('******************************')
