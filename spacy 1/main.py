import tika
from tika import parser
import spacy

tika.initVM()
nlp = spacy.load("en_core_web_sm")

def extract_text_from_tif(tif_file_path):
    parsed = parser.from_file(tif_file_path)
    return parsed['content']

def annotate_grantor_and_grantee(text):
    doc = nlp(text)
    grantor = []
    grantee = []
    
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            grantor.append(ent.text)
        elif ent.label_ == 'ORG':
            grantee.append(ent.text)
    
    return grantor, grantee

def main():
    tif_file_path = r"C:\Users\ponsi\Downloads\test_doc_query_2"
    text_content = extract_text_from_tif(tif_file_path)
    
    grantors, grantees = annotate_grantor_and_grantee(text_content)
    
    print("Grantors:", grantors)
    print("Grantees:", grantees)

if __name__ == "__main__":
    main()
