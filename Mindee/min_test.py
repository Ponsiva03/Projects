from mindee import Client, documents

# Init a new client and add your custom endpoint (document)
mindee_client = Client(api_key="0f8afbcf54cf846897fdefb97de4b8a4").add_endpoint(
    account_name="ponsiva03",
    endpoint_name="grantor_grantee_name",
)

# Load a file from disk and parse it.
# The endpoint name must be specified since it cannot be determined from the class.
result = mindee_client.doc_from_path(r"C:\python files\Mindee\Mindee Images\3053369_631378.tif").parse(documents.TypeCustomV1, endpoint_name="grantor_grantee_name")

# Print a brief summary of the parsed data
print(result.document)

# Iterate over all the fields in the document
for field_name, field_values in result.document.fields.items():
    print(field_name, "=", field_values)