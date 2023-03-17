def process_txt(file, delimiters):
    with open(file, "r") as f:
        content = f.read()
    return content
