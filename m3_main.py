from os import path, chdir, listdir, getcwd
from math import log, sqrt, pow
import json
import string
import pprint
import re
import unidecode

# Custom Classes
from positional_inverted_index import positional_inverted_index
from index_writer import index_writer
from kgram_index import kgram_index
from rank import rank
from query import Query

# Porter 2 Stemmer
from porter2stemmer import Porter2Stemmer
import time

# The Index
# { index[term] : [<ID, [p1, p2,... pk]>, <ID, [p1, p2,... pk]>, ...] }
index = positional_inverted_index()

# List of vocab tokens for terms in the corpus
# Dictionary <String : Set<String>>
avg_doc_length = 0


# Use this index_file for .json files
def index_file(file_name, documentID):
    stemmer = Porter2Stemmer()
    k = kgram_index()

    # Dealing with punctuation
    p = dict.fromkeys(string.punctuation)
    p.pop('-')  # we need to deal with hyphens
    punctuation = str.maketrans(p)
    weight_map = {}

    try:
        with open(file_name) as json_file:
            article_data = json.load(json_file)
            body = unidecode.unidecode(article_data['body']).lower().translate(punctuation).split(' ')
            body = list(filter(lambda t: t != '' and t != '-', body)) # remove single spaces and single hyphens

            #kgram stuff here

            position = 0
            for term in body:
                # take care of hyphenated words
                if '-' in term:
                    unhyphenated_word = term.replace('-', '')
                    index.add_term(stemmer.stem(unhyphenated_word), documentID, position)
                    hyphened_tokens = term.split('-')
                    for t in hyphened_tokens:
                        index.add_term(stemmer.stem(t), documentID, position)
                else:
                    index.add_term(stemmer.stem(term), documentID, position)
                position += 1
                if term not in weight_map:
                    weight_map[term] = 1
                else:
                    weight_map[term] = weight_map[term] + 1

    except FileNotFoundError as e:
        print(e)

    wdt = 0
    i_writer = index_writer()
    # Gets the Wdt's of the terms in the file
    for tf in weight_map:
        wdt += pow(1 + log(weight_map[tf]), 2)
    Ld = sqrt(wdt)
    i_writer.write_ld(Ld)


# If the user selects a certain document, for displaying the original content
def open_file_content(file_name):
    with open(file_name, 'r') as json_file:
        article_data = json.load(json_file)
        print(article_data['title'] + '\n')
        print (article_data['body'] + '\n')
        print (article_data['url'] + '\n')



def document_parser(id):
    return str('json' + str(id) + '.json')


def init(directory):
    file_names = []  # Names of files
    index.clean()
    vocab = {}
    chdir(directory)
    sorted_files = sorted(listdir(directory), key=lambda x: (int(re.sub('\D', '', x)), x))

    for file in sorted_files:
        if file.endswith('.json'):
            file_names.append(str(file))

    # Index each file and mark its Document ID
    for file in file_names:
        index_file(file, int(re.findall(r'\d+', file)[0]))


def main():
    # Instances
    # directory = input('Enter directory for index: ')  # TODO Revert back to original when done

    # TODO This is for testing purposes, so i can compare output
    # test_dir = '/Users/Cemo/Documents/cecs429/search_engine/corpus/mlb_documents'
    # test_dir = '/Users/Cemo/Documents/cecs429/search_engine/corpus/kumin'
    # test_dir = '/Users/Cemo/Documents/cecs429/search_engine/corpus/disk_test'

    cwd = getcwd()
    start_time = time.time()

    corpus_size = len(listdir('/Users/Cemo/Documents/cecs429/search_engine/corpus/all-nps-sites'))

    # init(test_dir)
    print("--- %s seconds ---" % str((time.time() - start_time) / 60))

    while 1:
        chdir(cwd)  # Changing to the directory of with the DB file in it for sqlite
        query_or_index = input('[1] - Query\n[2] - Index\n')
        print(query_or_index)
        if query_or_index == '1':

            query_type = input('[1] - Rank\n[2] - Boolean\n')
            if query_type == '1':
                r = rank()
                q = input('Enter query: ')
                r.get_rank(q, corpus_size)
                # print(r.get_rank(q, corpus_size))

                # print(r.get_rank('wildfire in yosemite', corpus_size))
            else:
                return_docs = []

                user_string = input("Please enter a word search:\n")
                # Special Queries
                if ':' in user_string:
                    if ':q' in user_string:
                        exit()
                    if ':stem' in user_string:
                        stemmer = Porter2Stemmer()
                        print("Will be stemming the token")
                        print(user_string.split(" ")[1])
                        print(stemmer.stem(user_string.split(" ")[1]))
                    if ':index' in user_string:
                        print('Will be indexing folder')
                        init(user_string.split(" ")[1].rstrip().lstrip())
                    if ':vocab' in user_string:
                        pp = pprint.PrettyPrinter(indent=4)
                        pp.pprint(index.get_dictionary())
                        print('Total number of vocabulary terms: ' + str(index.get_term_count()))
                        print('Will be spitting out words')
                else:
                    if user_string:
                        q = Query()
                        return_docs = q.query_parser(user_string)
                    else:
                        print('No query entered')

                print('DOC_LIST: ' + str(return_docs))

                # Allow the user to select a document to view
                doc_list = list(map(document_parser, return_docs))
                if len(doc_list) != 0:
                    for document in doc_list:
                        print ('Document ' + document)
                    print ('Documents found: ' + str(len(doc_list)))
                    document_selection = input('Please select a document you would like to view: ')
                    while document_selection != 'no':
                        if document_selection in doc_list:
                            open_file_content(document_selection)
                        document_selection = input('Please select a document you would like to view: ')
                else:
                    print ('No documents were found')
        else:
            print('Please dont')
            directory = input('Enter directory for index: ')  # TODO Revert back to original when done
            init(directory)
            i_writer = index_writer()
            i_writer.write_index_to_disk(index.get_index())


if __name__ == "__main__":
    main()
