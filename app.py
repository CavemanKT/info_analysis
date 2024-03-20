import pdfplumber
from collections import Counter
import spacy
from sklearn.metrics.pairwise import cosine_similarity


# import re
# import os
# from flask import Flask, render_template, request
# from werkzeug.utils import secure_filename

# app = Flask(__name__)

# check a file if it is a pdf
def is_pdf(file_path):
    """
    Check if a file is a pdf
    """
    with open(file_path, 'rb') as f:
        return f.read(4) == b'%PDF'

isPdfType = is_pdf('test.pdf')
print("🐍 File: info_analysis/app.py | Line: 23 | undefined ~ pdfType",isPdfType)

with pdfplumber.open('test.pdf') as pdf:
    text_content = ""
    for page in pdf.pages:
        text_content += page.extract_text()

words = text_content.split()  # Split text into individual words
word_frequency = Counter(words)

# import en_core_web_sm
nlp = spacy.load('en_core_web_sm')

# nlp = en_core_web_sm.load()
max_similarity = 0
for word in words:
    doc = nlp(word)
    searchWord = nlp("sed")
    similarity = searchWord.similarity(doc)
    if similarity > max_similarity:
        max_similarity = similarity
        print("🐍 File: python/app.py | Line: 31 | undefined ~ similarity",similarity, word)

# word1 = nlp('lorem')
# word2 = nlp('word')
# similarity = word1.similarity(word2)
# print("🐍 File: python/app.py | Line: 31 | undefined ~ similarity",similarity)