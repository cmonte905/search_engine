from os import path, chdir, listdir, getcwd
from math import log, sqrt, pow
import json
import string
import pprint
import re
import unidecode

# Custom Classes
from positional_inverted_index import positional_inverted_index
from disk_inverted_index import disk_inverted_index
from posting import posting
from index_writer import index_writer
from kgram_index import kgram_index
from wildcard import wildcard
from near import near
from pos_db import position_db

# Porter 2 Stemmer
from porter2stemmer import Porter2Stemmer

from query import Query
import time

# The Index
# { index[term] : [<ID, [p1, p2,... pk]>, <ID, [p1, p2,... pk]>, ...] }
index = positional_inverted_index()

# List of vocab tokens for terms in the corpus
# Dictionary <String : Set<String>>
vocab = {}

pp = pprint.PrettyPrinter(indent=4)

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
                #kgram stuff here
                kgram_list = []
                # develop a list of kgram tokens for one specific term
                # kgram doesn't need to deal with hyphens because the tokens will be created anyways
                for i in range(1, 4):
                    if i is 1:
                        kgram_list.extend(k.create_kgram(term, i))
                    else:
                        s = ('$' + term + '$')
                        kgram_list.extend(k.create_kgram(s, i))
                # Shove each of those tokens into the grand vocab dictionary
                for token in kgram_list:
                    if token in vocab:
                        vocab[token].add(term)
                    else:
                        vocab[token] = set([term])

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
                if not weight_map.get(term):
                    weight_map[term] = 1
                else:
                    weight_map[term] += 1

    except FileNotFoundError as e:
        print(e)
    wdt = 0
    i_writer = index_writer()
    # Gets the Wdt's of the terms in the file
    for tf in weight_map:
        wdt += pow(1 + log(weight_map[tf]), 2)
    print('Wdt: ', wdt)
    Ld = sqrt(wdt)
    print('Ld of ', file_name, ':', Ld)
    i_writer.write_ld(Ld)


# If the user selects a certain document, for displaying the original content
def open_file_content(file_name):
    with open(file_name, 'r') as json_file:
        article_data = json.load(json_file)
        print(article_data['title'] + '\n')
        print (article_data['body'] + '\n')
        print (article_data['url'] + '\n')

# Wild card input
# word_input: the user input of a wild card. 
# EX:   land*cape
#       he*lo
def wild(word_input):
    kg = kgram_index()
    w = wildcard()
    stemmer = Porter2Stemmer()

    ktokens = []
    wildcard_tokens = w.wildcard_parser(word_input)

    for token in wildcard_tokens:
        k = 0
        if len(token) > 3:
            k = 3
        else:
            k = len(token)
        ktokens.extend(kg.create_kgram(token, k))

    # remove '$' from tokens
    ktokens[:] = [x for x in ktokens if x != '$']

    canidate_lists = []

    for token in ktokens:
        if token in vocab:
            canidate_lists.append(vocab[token])
            print(token, list(vocab[token]), len(vocab))

    intersected_list = list(set(canidate_lists[0].intersection(*canidate_lists[1:])))

    n = list(map(lambda t: stemmer.stem(t), intersected_list))
    n = list(map(lambda t: index.get_index()[t], n))

    doc_list = []
    for p_list in n:
        for post in p_list:
            doc_list.append(post.get_document_id())
    # return list of docs for the word found
    return doc_list

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
    w = wildcard()
    n = near()

    # directory = input('Enter directory for index: ')  # TODO Revert back to original when done

    # TODO This is for testing purposes, so i can compare output
    # test_dir = '/Users/Cemo/Documents/cecs429/search_engine/corpus/mlb_documents'
    test_dir = '/Users/Cemo/Documents/cecs429/search_engine/corpus/disk_test'
    cwd = getcwd()
    start_time = time.time()
    init(test_dir)
    chdir(cwd)  # Changing to the directory of with the DB file in it for sqlite
    print("--- %s seconds ---" % str((time.time() - start_time) / 60))

    # Find all .json files in this directory
    # directory = path.dirname(path.realpath(__file__)) + '/corpus/all-nps-sites/'
    #directory = path.dirname(path.realpath(__file__))

    #print (index.get_all_doc_ids('park').intersection(index.get_all_doc_ids('sand')))

    #print (index.get_all_doc_ids_index('park'))
    #print (n.near(index, 'explore', 'park', 6))

    #for key in index.get_index():
    #    index.print_term_info(key)

    # ------------------------------------------------------------------------------------------------------------
    # Writes to the DB and file

    # i_writer = index_writer()
    # i_writer.write_index_to_disk(index.get_index())

    # Reads from bin files and DB
    i_reader = disk_inverted_index()
    print('Term that we get back: warn')
    print(i_reader.read_with_pos('warn'))
    print(i_reader.read_without_pos('warn'))
    for i in i_reader.get_pos_postings_from_disk('warn'):
        print(i)
    print(i_reader.read_ld(1))
    print(i_reader.read_ld(2))
    print(i_reader.read_ld(3))
    print(i_reader.read_ld(4))
    print(i_reader.read_ld(5))

    # ------------------------------------------------------------------------------------------------------------

    # while 1:
    #
    #     return_docs = []
    #
    #     user_string = input("Please enter a word search:\n")
    #     # Special Queries
    #     if ':' in user_string:
    #         if ':q' in user_string:
    #             exit()
    #         if ':stem' in user_string:
    #             stemmer = Porter2Stemmer()
    #             print("Will be stemming the token")
    #             print(user_string.split(" ")[1])
    #             print(stemmer.stem(user_string.split(" ")[1]))
    #         if ':index' in user_string:
    #             print('Will be indexing folder')
    #             init(user_string.split(" ")[1].rstrip().lstrip())
    #         if ':vocab' in user_string:
    #             pp = pprint.PrettyPrinter(indent=4)
    #             pp.pprint(index.get_dictionary())
    #             print('Total number of vocabulary terms: ' + str(index.get_term_count()))
    #             print('Will be spitting out words')
    #     elif '*' in user_string:
    #         print("This will get sent of to the wildcard class")
    #         return_docs.extend(wild(user_string))
    #     elif 'near' in user_string:
    #         # Parse NEAR input
    #         near_parts = user_string.split(' ')
    #         k = near_parts[1].split('/')
    #         return_docs.extend(n.near(index, near_parts[0], near_parts[2], int(k[1])))
    #     else:
    #         if user_string:
    #             q = Query(index)
    #             return_docs = q.query_parser(user_string)
    #             #for i in results_list:
    #                 #print('json' + str(i) + '.json')
    #             #print('Num of results:\n', len(results_list))
    #         else:
    #             print('No query entered')
    #
    #     print ('DOC_LIST: ' + str(return_docs))
    #
    #     # Allow the user to select a document to view
    #     doc_list = list(map(document_parser, return_docs))
    #     if len(doc_list) != 0:
    #         for document in doc_list:
    #             print ('Document ' + document)
    #         print ('Documents found: ' + str(len(doc_list)))
    #         document_selection = input('Please select a document you would like to view: ')
    #         while document_selection != 'no':
    #             if document_selection in doc_list:
    #                 open_file_content(document_selection)
    #             document_selection = input('Please select a document you would like to view: ')
    #     else:
    #         print ('No documents were found')


if __name__ == "__main__":
    main()