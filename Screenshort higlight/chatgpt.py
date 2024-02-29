import pdfkit
import fitz  # PyMuPDF
import requests
import tempfile
import os

def download_html_content(url):
    response = requests.get(url)
    return response.text

def convert_html_to_pdf(html_link, output_pdf_path='output.pdf', highlight_word=None):
    # Download HTML content
    html_content = download_html_content(html_link)

    # Convert HTML to PDF with --no-images option
    options = {'no-images': ''}
    pdfkit.from_string(html_content, output_pdf_path, options=options)

    # Open the PDF with PyMuPDF
    pdf_document = fitz.open(output_pdf_path)

    # Iterate through pages and highlight the specified word
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        text_instances = page.search_for(highlight_word)

        for inst in text_instances:
            highlight_rect = inst.rect
            highlight_annot = page.add_highlight_annot(highlight_rect)

    # Save the final PDF
    pdf_document.save(output_pdf_path)

# Example usage
html_link = input("Enter the HTML link: ")
highlight_word = input("Enter the word to highlight: ")
output_pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
convert_html_to_pdf(html_link, output_pdf_path, highlight_word)

print(f"PDF with highlighted word saved at: {output_pdf_path}")
