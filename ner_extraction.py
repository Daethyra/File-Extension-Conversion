# Import your NER library and implement the NER function
# This example uses the spaCy library

import spacy

nlp = spacy.load("en_core_web_sm")

def extract_named_entities(text):
    doc = nlp(text)
    named_entities = [(ent.text, ent.label_) for ent in doc.ents]
    return named_entities
