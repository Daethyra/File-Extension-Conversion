import spacy

class TextProcessor:
    """
    The TextProcessor class handles the processing of text (lemmatization and stop words removal).
    """
    def __init__(self):
        # Load spaCy model for stop words removal and lemmatization.
        self.nlp = spacy.load('en_core_web_sm')

    def process_text(self, text):
        """
        Process the extracted text by lemmatization and stop words removal using spaCy.
        """
        doc = self.nlp(text)
        processed_text = ' '.join([token.lemma_ for token in doc if not token.is_stop])
        return processed_text
