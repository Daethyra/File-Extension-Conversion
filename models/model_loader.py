from transformers import AutoModelForSequenceClassification, AutoTokenizer

def load_model(model_path):
    """
    Load a locally saved language model.
    """
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return model, tokenizer
