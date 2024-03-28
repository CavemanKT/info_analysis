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

SAMPLE_DATA_PATH='./sampleData/2021-09-22_Paper_12.pdf'

isPdfType = is_pdf(SAMPLE_DATA_PATH)
print("🐍 File: info_analysis/app.py | Line: 23 | undefined ~ pdfType",isPdfType)

with pdfplumber.open(SAMPLE_DATA_PATH) as pdf:
    text_content = ""
    table_content = []
    no_of_pages = len(pdf.pages)
    for page in pdf.pages:
        page_number = page.page_number
        print(page_number)

        text = page.extract_text()
        text_content += text
        table_content.append(page.extract_table())
        for line in text.split('\n'):
            print(line)

words = text_content.split()  # Split text into individual words
# print(words)


word_frequency = Counter(words)

# print(table_content)

# print(no_of_pages)

print(word_frequency)
