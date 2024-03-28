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

SAMPLE_DATA_PATH='./sampleData/Handbook_Gas_Utilisation_Facilities.pdf'

isPdfType = is_pdf(SAMPLE_DATA_PATH)
print("🐍 File: info_analysis/app.py | Line: 23 | undefined ~ pdfType",isPdfType)

filename = Path(SAMPLE_DATA_PATH).name
print("filename: ", filename)


# check if most of the text is in Chinese or English
language_setting = 'english'
extracted_text = extract_text(SAMPLE_DATA_PATH)
detectors = Detector(extracted_text).languages
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


# start processing pdf, generate json to prepare indexing
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
            

            # # Create a parser and tokenize the text
            parser = PlaintextParser.from_string(text, Tokenizer(language_setting))

            # Access the parsed document
            document = parser.document

            # Summarize using sumy LSA
            summary =summarizer_lsa(document,2)
            lsa_summary=""            
            for sentence in summary:     
                lsa_summary+=str(sentence)                 
                # print(lsa_summary)
            obj = {
                "summary": lsa_summary,
                "page_number": page_number,
                "content": text
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

# clear index
def clear_index():
  es.indices.delete(index='demo_index', ignore_unavailable=True)

# create index
def create_index():
  es.indices.create(
    index='demo_index',
    mappings={
      'properties': {
        'embedding': {
          'type': 'dense_vector',
        }
      }
    },
    settings={
      'number_of_shards': 1,
      'number_of_replicas': 0
    }
  )

def get_embedding(text):
    return model.encode(text)
  
def insert_documents(documents):
    operations = []
    # self.process_pipeline('data_pipeline')
    for document in documents:
        operations.append({'index': {'_index': 'demo_index' }})
        # operations.append({'index': {'_index': 'my_documents', "pipeline": "data_pipeline" }})
        operations.append({
        **document,
        'embedding': get_embedding(document['summary'])
        })
    return es.bulk(operations=operations)

def reindex():
    create_index()
    
    files = os.listdir('./input')
    for file in files:
        if file.endswith("Handbook_Gas_Utilisation_Facilities.json"):
            print(file)
            with open(f'./input/{file}', 'rt') as f:
                documents = json.loads(f.read())
                print(documents)
            insert_documents(documents)
    return True

clear_index()
reindex()

with open(SAMPLE_DATA_PATH, 'rb') as f:
  doc = {
    'data': f.read()
  }
#   requests.put(
#     'http://localhost:9200/my-index-000001/_doc/my_id?pipeline=cbor-attachment',
#     data=cbor2.dumps(doc),
#     headers=headers
#   )
