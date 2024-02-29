

from flask import Flask, render_template, request, redirect, send_from_directory, session, url_for, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for flashing messages

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
processed_data = None  # Global variable to store processed data (for demonstration purposes)

def create_template_file():
    template_data = {
        'SKU_ID': [],
        'MPN': [],
        'Sample_URL_Column': []  # Replace with an actual column name
    }
    df_template = pd.DataFrame(template_data)

    # Save the DataFrame to a template file
    template_file_path = 'template.xlsx'  # Change the file extension as needed
    df_template.to_excel(template_file_path, index=False)

create_template_file()

@app.route('/', methods=['GET', 'POST'])
def map_input_data():
    global processed_data

    if request.method == 'POST':
        # Process file upload
        file = request.files['input-file-path']
        if file and allowed_file(file.filename):
            try:
                # Read and process the file data
                processed_data = process_file(file)
                
                flash('Excel file passed successfully!', 'success')
                session['processing_success'] = True
            except ValueError as ve:
                # If the process_file function raises a ValueError,
                # handle the specific error messages
                flash(str(ve), 'danger')
        else:
            flash('Invalid file format', 'danger')

    # Check if the session variable indicates successful processing
    if session.get('processing_success'):
        # Clear the session variable after using it
        session.pop('processing_success', None)
        return redirect(url_for('set_output_path'))

    return render_template('index.html')

@app.route('/set_output_path', methods=['GET', 'POST'])
def set_output_path():
    global processed_data
    alert_message = None

    if request.method == 'POST':
        # Get the user-entered output path from the form
        output_path = request.form.get('output-path')

        if output_path:
            try:
                # Save the processed data to a new CSV file in the specified output path
                save_to_csv(processed_data, output_path)

                alert_message = f"Data saved to CSV file in: {output_path}"
            except Exception as e:
                alert_message = f"Error saving data: {str(e)}"
        else:
            alert_message = "Please enter a valid output path."

    return render_template('set_output_path.html', alert_message=alert_message)

# Add a new function to save processed data to a CSV file
def save_to_csv(processed_data, output_path):
    df_processed = pd.DataFrame(processed_data)
    csv_file_path = os.path.join(output_path, 'processed_data.csv')
    df_processed.to_csv(csv_file_path, index=False)

@app.route('/download_template', methods=['GET'])
def download_template():
    # Create the template file if it doesn't exist
    if not os.path.exists('template.xlsx'):
        create_template_file()  # Call the existing function to create the file

    # Send the template file for download
    return send_from_directory('.', 'template.xlsx', as_attachment=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(file):
    # Read the file into a DataFrame
    df = pd.read_excel(file)

    # Check for the required columns
    required_columns = ['SKU_ID', 'MPN']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Excel file should have the column: '{col}'")

    # Check for at least one column with 'URL' in its name
    url_columns = [col for col in df.columns if 'URL' in col.upper()]
    if not url_columns:
        raise ValueError("Excel file should have at least one column with 'URL' in its name")

    return df.to_dict('records')  # For demonstration, returning processed data

if __name__ == '__main__':
    app.run(debug=True)
