from flask import Flask, render_template, request, redirect, send_from_directory, session, url_for, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = '1234'  # Set a secret key for flashing messages

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
processed_data = None  # Global variable to store processed data (for demonstration purposes)

def create_template_file():
    template_data = {
        'SKU_ID': [],
        'MPN': [],
        'Sample_URL_': [] 
    }
    df_template = pd.DataFrame(template_data) # Save the DataFrame to a template file

    template_file_path = 'template.xlsx'  # Change the file extension as needed
    df_template.to_excel(template_file_path, index=False)
create_template_file()

@app.route('/', methods=['GET', 'POST'])
def map_input_data():
    global processed_data

    if request.method == 'POST': # Process file upload
        file = request.files['input-file-path']
        if file and allowed_file(file.filename):
            try:
                processed_data = process_file(file)# Read and process the file data
        
                flash('Excel file passed successfully!', 'success')
           
                return redirect(url_for('set_output_path'))
            except ValueError as ve:
                
                flash(str(ve), 'danger')
        else:
            flash('Invalid file format', 'danger')

   
    return render_template('index.html')

@app.route('/set_output_path', methods=['GET', 'POST'])
def set_output_path():
    global processed_data
    alert_message = None

    if request.method == 'POST':
       
        output_path = request.form.get('output-path') # Get the user-entered output path from the form

        if output_path:
        
            alert_message = f"Output will be saved to: {output_path}"
        else:
            alert_message = "Please enter a valid output path."

    return render_template('set_output_path.html', alert_message=alert_message)




@app.route('/download_template', methods=['GET'])
def download_template():
   
    if not os.path.exists('template.xlsx'): # Create the template file if it doesn't exist
        create_template_file()  # Call the existing function to create the file

    return send_from_directory('.', 'template.xlsx', as_attachment=True)    # Send the template file for download



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(file):
   
    df = pd.read_excel(file) # Read the file into a DataFrame

   
    required_columns = ['SKU_ID', 'MPN'] # Check for the required columns
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Excel file should have the column: '{col}'")

   
    url_columns = [col for col in df.columns if 'URL' in col.upper()] # Check for at least one column with 'URL' in its name
    if not url_columns:
        raise ValueError("Excel file should have at least one column with 'URL' in its name")
        return df.to_dict('records')  # For demonstration, returning processed data

if __name__ == '__main__':
    app.run(debug=True)
