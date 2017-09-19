import json
import os.path
# from pprint import pprint

def read_corpus():
    print 1
    with open('all-nps-sites.json') as data_file:    
        corpus_data = json.load(data_file)
    print len(corpus_data['documents'])
    return corpus_data

def read_mlb_corpus(self):
    corpus_data = {}

    print 1 
