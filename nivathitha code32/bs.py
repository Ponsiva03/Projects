import pdfkit

# URL of the HTML page
url = "https://www.lg.com/us/air-conditioners/lg-lw1017ersm1-window-air-conditioner"

# Output PDF file path
output_file_path = "output.pdf"

# Convert HTML from URL to PDF
try:
    pdfkit.from_url(url, output_file_path)
    print(f"PDF created successfully at: {output_file_path}")
except Exception as e:
    print(f"Error creating PDF: {e}")
