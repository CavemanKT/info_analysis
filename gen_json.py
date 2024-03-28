import json
import pdfplumber
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

from pdfminer.high_level import extract_text

# summarize content
from sumy.summarizers.lsa import LsaSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
import nltk
nltk.download('punkt')
nltk.download('jieba')


summarizer_lsa = LsaSummarizer()

from polyglot.detect import Detector

# import re
import os
# from flask import Flask, render_template, request
# from werkzeug.utils import secure_filename

# app = Flask(__name__)

# create a folder called input
if not os.path.exists('./input'):
    os.makedirs('input')

# check a file if it is a pdf
def is_pdf(file_path):
    """
    Check if a file is a pdf
    """
    with open(file_path, 'rb') as f:
        return f.read(4) == b'%PDF'

language_setting = 'english'

def set_language(detectors):
    print(detectors[2])
    bytes_of_language1 = [detectors[0].name, detectors[0].read_bytes]
    print("🐍 File: info_analysis/app.py | Line: 62 | undefined ~ bytes_of_language1",bytes_of_language1)
    bytes_of_language2 = [detectors[1].name, detectors[1].read_bytes]
    print("🐍 File: info_analysis/app.py | Line: 64 | undefined ~ bytes_of_language2",bytes_of_language2)
    if(bytes_of_language1[1] > bytes_of_language2[1]):
        if(bytes_of_language1[0] != "Chinese" and bytes_of_language1[0] != "English"):
            language_setting = 'english'
        else:
            language_setting = bytes_of_language1[0].lower()
    else:
        if(bytes_of_language2[0] != 'Chinese' and bytes_of_language2[0] != 'English'):
            language_setting = 'english'
        else:
            language_setting = bytes_of_language2[0].lower()
    return language_setting

# get all files in sampleData directory
sampleDataPath = os.listdir('./sampleData')
print(sampleDataPath)

for idx, sample_filename in enumerate(sampleDataPath):
    sample_file_path = f'./sampleData/{sample_filename}'
    isPdfType = is_pdf(sample_file_path)
    print("🐍 File: info_analysis/app.py | Line: 23 | undefined ~ pdfType",isPdfType)

    filename = Path(sample_file_path).name
    print("filename: ", filename)

    # check if most of the text is in Chinese or English
    extracted_text = extract_text(sample_file_path)
    try: 
        detectors = Detector(extracted_text).languages
        language_setting = set_language(detectors)
    except: 
        print("the input text is not text or string, skip this file and use english setting.")
    else :
        print("else: ", language_setting)
        print("🐍 File: info_analysis/app.py | Line: 62 | undefined ~ language_setting",language_setting)

    


    # start processing pdf, generate json to prepare indexing
    if not False or os.path.exists(f"./input/{filename[:-4]}.json"):
        # make the json file
        with open(f"./input/{filename[:-4]}.json", 'w') as f:
            f.write('[]')
        with pdfplumber.open(sample_file_path) as pdf:
            text_content = ""
            table_content = []
            total_pages = len(pdf.pages)
            for idx, page in enumerate(pdf.pages):
                page_number = page.page_number

                text = page.extract_text()
                

                # # Create a parser and tokenize the text
                parser = PlaintextParser.from_string(text, Tokenizer(language_setting))

                # Access the parsed document
                document = parser.document

                # Summarize using sumy LSA
                summary = summarizer_lsa(document,1)
                lsa_summary=""
                for sentence in summary:     
                    lsa_summary+=str(sentence)                 
                    # print(lsa_summary)


                obj = {
                    "filename": filename[:-4],
                    "file_number": idx,
                    "summary": lsa_summary,
                    "content": text,
                    "page_number": page_number,
                    "total_pages": total_pages,
                    "tag": filename.split(".")[-1],
                }

                with open(f"./input/{filename[:-4]}.json", 'r') as f:
                    data = json.load(f)
                data.append(obj)
                with open(f"./input/{filename[:-4]}.json", 'w', encoding='utf8') as f:
                    json.dump(data, f, ensure_ascii=False)
                text_content += text
                table_content.append(page.extract_table())
                # for line in text.split('\n'):
                    # print(line)
        words = text_content.split()  # Split text into individual words
        word_frequency = Counter(words)
    else: 
        with open(f"./input/{filename[:-4]}.json", 'r') as f:
            text_content = f.read()
            print("🐍 File: info_analysis/app.py | Line: 90 | undefined ~ text_content",text_content)



