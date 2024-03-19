import pdfplumber
from collections import Counter
import spacy
from sklearn.metrics.pairwise import cosine_similarity


# import re
# import os
# from flask import Flask, render_template, request
# from werkzeug.utils import secure_filename

# app = Flask(__name__)

with pdfplumber.open('webDev.pdf') as pdf:
    text_content = ""
    for page in pdf.pages:
        text_content += page.extract_text()
    print(text_content)

words = text_content.split()  # Split text into individual words
word_frequency = Counter(words)

# import en_core_web_sm
nlp = spacy.load('en_core_web_sm')

# nlp = en_core_web_sm.load()

word1 = nlp('word')
word2 = nlp('word')
similarity = word1.similarity(word2)
print("🐍 File: python/app.py | Line: 31 | undefined ~ similarity",similarity)