import json
import os.path
# from pprint import pprint

def read_corpus(self):
    with open('all-nps-sites.json') as data_file:    
        corpus_data = json.load(data_file)
    return corpus_data

