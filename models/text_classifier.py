import torch
from model_loader import load_model

class TextClassifier:
    """
    The TextClassifier class uses a loaded language model to classify text.
    """
    def __init__(self, model_path):
        self.model, self.tokenizer = load_model(model_path)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    def classify_event(self, text):
        """
        Classify the input event as 'push' or 'other'.
        """
        inputs = self.tokenizer(text, return_tensors='pt').to(self.device)
        outputs = self.model(**inputs)
        _, predicted = torch.max(outputs.logits, 1)
        if predicted.item() == 0:
            return 'push'
        else:
            return 'other'
