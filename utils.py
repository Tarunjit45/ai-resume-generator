import re

def extract_keywords(text):
    # Simple keyword extractor: returns unique words longer than 3 characters
    words = re.findall(r'\\b\\w{4,}\\b', text.lower())
    return list(set(words))
