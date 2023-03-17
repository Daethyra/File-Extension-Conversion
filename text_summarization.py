# Import your text summarization library and implement the summarization function
# This example uses the Gensim library

from gensim.summarization import summarize

def summarize_text(text):
    summary = summarize(text)
    return summary
