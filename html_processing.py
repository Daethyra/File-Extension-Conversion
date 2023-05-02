from bs4 import BeautifulSoup

def process_html(file, delimiters):
    with open(file, "r") as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text()
    return text
