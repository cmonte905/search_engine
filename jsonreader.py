import json
import os.path
# from pprint import pprint

def read_corpus():
    with open('json1.json') as data_file:    
        corpus_data = json.load(data_file)
    print (corpus_data['body'])

    print (type(corpus_data['body']))
    print (corpus_data['body'].lower().split(' '))

    return corpus_data

def read_mlb_corpus(self):
    corpus_data = {}

    print (1)


read_corpus()