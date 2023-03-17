from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from string import punctuation

def tokenize_and_normalize(text):
    # Tokenization
    words = word_tokenize(text)
    
    # Normalization
    lower_words = [word.lower() for word in words]
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in lower_words if word not in stop_words]
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in filtered_words]
    
    return stemmed_words
