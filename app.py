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
    # with open("./input/Handbook_Gas_Utilisation_Facilities.json", 'rb') as f:    
    #     documents = json.loads(f.read())
    # return insert_documents(documents)

    files = os.listdir('./input')
    for file in files:
        if file.endswith(".json"):
            with open(f'./input/{file}', 'rt') as f:
                documents = json.loads(f.read())
            insert_documents(documents)
    return True

clear_index()
reindex()

SAMPLE_DATA_PATH='./sampleData/Handbook_Gas_Utilisation_Facilities.pdf'

with open(SAMPLE_DATA_PATH, 'rb') as f:
  doc = {
    'data': f.read()
  }
#   requests.put(
#     'http://localhost:9200/my-index-000001/_doc/my_id?pipeline=cbor-attachment',
#     data=cbor2.dumps(doc),
#     headers=headers
#   )
