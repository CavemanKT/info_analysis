import json
import pdfplumber
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

from pdfminer.high_level import extract_text
import pdfminer

from sumy.summarizers.lsa import LsaSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
import nltk
# nltk.download('punkt')
nltk.download('jieba')


summarizer_lsa = LsaSummarizer()                   



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

SAMPLE_DATA_PATH='./sampleData/Handbook_Gas_Utilisation_Facilities.pdf'

isPdfType = is_pdf(SAMPLE_DATA_PATH)
print("🐍 File: info_analysis/app.py | Line: 23 | undefined ~ pdfType",isPdfType)

filename = Path(SAMPLE_DATA_PATH).name
print("filename: ", filename)

if not False or os.path.exists(f"./input/{filename[:-4]}.json"):
    # make the json file
    with open(f"./input/{filename[:-4]}.json", 'w') as f:
        f.write('[]')
    with pdfplumber.open(SAMPLE_DATA_PATH) as pdf:
        text_content = ""
        table_content = []
        total_pages = len(pdf.pages)
        for page in pdf.pages:
            page_number = page.page_number

            text = page.extract_text()
            # Create a parser and tokenize the text
            parser = PlaintextParser.from_string(text, Tokenizer('chinese'))

            # Access the parsed document
            document = parser.document

            # Summarize using sumy LSA
            summary =summarizer_lsa(document,2)
            lsa_summary=""            
            for sentence in summary:                   
                lsa_summary+=str(sentence)                 
                print(lsa_summary)
            obj = {
                "summary": lsa_summary,
                "page_number": page_number,
                "text": text
            }

            with open(f"./input/{filename[:-4]}.json", 'r') as f:
                data = json.load(f)
            data.append(obj)
            with open(f"./input/{filename[:-4]}.json", 'w') as f:
                json.dump(data, f)
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




import cbor2
import requests

import json
from pprint import pprint
import os
import time

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

from sentence_transformers import SentenceTransformer


headers = {'content-type': 'application/cbor'}

es = Elasticsearch(['http://localhost:9200'])

model = SentenceTransformer('all-MiniLM-L6-v2')

client_info = es.info()
print('Connected to Elasticsearch!')
pprint(client_info.body)

# create index
def create_index():
  es.indices.create(
    index='demo-index',
    body={
      'mappings': {
        'properties': {
          'data': {
            'type': 'text'
          }
        }
      }
    }
  )


with open(SAMPLE_DATA_PATH, 'rb') as f:
  doc = {
    'data': f.read()
  }
#   requests.put(
#     'http://localhost:9200/my-index-000001/_doc/my_id?pipeline=cbor-attachment',
#     data=cbor2.dumps(doc),
#     headers=headers
#   )
