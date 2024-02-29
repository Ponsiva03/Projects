import spacy
import csv
import pandas as pd

def extract_names_from_csv(csv_file):
    nlp = spacy.load("en_core_web_lg")
    names = []

    with open(r"D:\python files\QA\notion-qa-master\langchain test\sample_res2.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            input_text = row["Grantor"] + " " + row["Grantee"]
            doc = nlp(input_text)
            for ent in doc.ents:
                   if ent.label_ in ["PERSON", "ORG"]:
                    names.append(ent.text)

    return names

# Example usage
csv_file = "data.csv"
names = extract_names_from_csv(csv_file)

# Saving names in a CSV file
output_file = "test2.csv"
df = pd.DataFrame(names, columns=["Name"])
df.to_csv(output_file, index=False)
