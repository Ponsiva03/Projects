# import pdfkit

# # The URL  of the HTML page you want to convert
# url =  "https://www.ti.com/product/ADS8664?keyMatch=ADS8664IDBT&tisearch=Search-EN-Everything"

# # The path where you want to save the PDF
# output_path = "output.pdf"



# # Convert the HTML page to a PDF
# pdfkit.from_url(url, output_path)




import pdfkit
import requests

def convert_html_to_pdf(input_path, output_path):
    """Converts HTML content to PDF, preserving design as much as possible.

    Args:
        input_path (str): Path to the HTML file or web URL.
        output_path (str): Path to save the generated PDF.
    """

    try:
        if input_path.startswith("http"):
            # Fetch HTML content from URL
            response = requests.get(input_path)
            content = response.content.decode('utf-8')  # Decode bytes to string
        else:
            # Read HTML content from local file
            with open(input_path, "r", encoding="utf-8") as f:
                content = f.read()

        # Use pdfkit to convert HTML to PDF, handling potential errors
        pdfkit.from_string(content, output_path)
        print(f"HTML content successfully converted to PDF and saved at: {output_path}")

    except Exception as e:
        print(f"Error converting HTML to PDF: {e}")

# Example usage:
input_path ="https://www.ti.com/product/ADS8664?keyMatch=ADS8664IDBT&tisearch=Search-EN-Everything" # Replace with your desired HTML path or URL
output_path = "output134.pdf"  # Replace with your desired output PDF path
convert_html_to_pdf(input_path, output_path)