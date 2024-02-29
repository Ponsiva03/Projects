import spacy
import pandas as pd

def apply_spacy(row):
    nlp = spacy.load("en_core_web_lg")
    grantor_text = row["Grantor"]
    grantee_text = row["Grantee"]
    doc_grantor = nlp(grantor_text)
    doc_grantee = nlp(grantee_text)
    
    grantor_entities = [ent.text for ent in doc_grantor.ents if ent.label_ == "PERSON" or ent.label_ == "ORG"]
    grantee_entities = [ent.text for ent in doc_grantee.ents if ent.label_ == "PERSON" or ent.label_ == "ORG"]
    
    return grantor_entities, grantee_entities

# Read the DataFrame
df = pd.read_csv(r"D:\python files\QA\notion-qa-master\langchain test\test data 2.csv")

# Apply spaCy over "Grantor" and "Grantee" columns and extract specified entities
df[["Grantor_Entities", "Grantee_Entities"]] = df.apply(apply_spacy, axis=1, result_type="expand")

# Save the DataFrame with the new columns to an Excel file
output_file = "spacy result 2.csv"
df.to_csv(output_file, index=False)
