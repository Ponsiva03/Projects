import os
import csv
from mindee import Client, documents

# Initialize the Mindee client
mindee_client = Client(api_key="0f8afbcf54cf846897fdefb97de4b8a4").add_endpoint(
    account_name="ponsiva03",
    endpoint_name="grantor_grantee_name",
)

# Input folder containing the TIFF files
input_folder = r'C:\python files\Mindee\mindee test'

# Output CSV file path
output_csv_file = "parsed_data.csv"

# Initialize a list to accumulate parsed data
parsed_data = []

# Function to format and print the output
def print_output(filename, grantor, grantee):
    print(f"----- grantor_grantee_name -----\nFilename: {filename}\ngrantee: {grantee}\ngrantor: {grantor}\n----------------------")

# Iterate through files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".tif"):
        file_path = os.path.join(input_folder, filename)
        
        # Parse the document
        result = mindee_client.doc_from_path(file_path).parse(
            documents.TypeCustomV1, endpoint_name="grantor_grantee_name"
        )

        # Extract grantor and grantee from the parsed data
        grantor = result.document.fields.get("grantor", "")
        grantee = result.document.fields.get("grantee", "")

        # Print the formatted output
        print_output(filename, grantor, grantee)

        # Append the parsed data to the list
        parsed_data.append({"grantee": grantee, "grantor": grantor})

# Save the parsed data to a CSV file
with open(output_csv_file, mode='w', newline='') as csv_file:
    fieldnames = ["grantee", "grantor"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the parsed data
    writer.writerows(parsed_data)

print(f"Data saved to {output_csv_file}")
