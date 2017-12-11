from os import chdir, listdir, getcwd
from math import log, sqrt, pow
import json
import string
import re
import unidecode
import pprint

# Custom Classes
from positional_inverted_index import positional_inverted_index
from index_writer import index_writer
from rank import rank

# Porter 2 Stemmer
from porter2stemmer import Porter2Stemmer
import time

# The Index
# { index[term] : [<ID, [p1, p2,... pk]>, <ID, [p1, p2,... pk]>, ...] }
all_docs_index = positional_inverted_index()
hamilton_index = positional_inverted_index()
jay_index = positional_inverted_index()
madison_index = positional_inverted_index()
disputed_index = positional_inverted_index()

# List of vocab tokens for terms in the corpus
# Dictionary <String : Set<String>>

# Use this index_file for .json files
def index_file(file_name, documentID, index):
    stemmer = Porter2Stemmer()
    # Dealing with punctuation
    p = dict.fromkeys(string.punctuation)
    p.pop('-')  # we need to deal with hyphens
    punctuation = str.maketrans(p)
    weight_map = {}

    try:
        with open(file_name) as txt_file:
            body = txt_file.read().split(' ')
            body = list(filter(lambda t: t != '' and t != '-', body))  # remove single spaces and single hyphens

            position = 0
            for term in body:
                # take care of hyphenated words
                if '-' in term:
                    unhyphenated_word = term.replace('-', '')
                    index.add_term(stemmer.stem(unhyphenated_word), documentID, position)
                    hyphened_tokens = term.split('-')
                    for t in hyphened_tokens:
                        all_docs_index.add_term(stemmer.stem(t), documentID, position)
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
    # i_writer = index_writer()
    # Gets the Wdt's of the terms in the file
    for tf in weight_map:
        wdt += pow(1 + log(weight_map[tf]), 2)
    Ld = sqrt(wdt)
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(weight_map)
    # print('\n\n Fuck -', file_name)
    # i_writer.write_ld(Ld)


def index_dir(file_name, documentID, index):
    stemmer = Porter2Stemmer()

    # Dealing with punctuation
    p = dict.fromkeys(string.punctuation)
    p.pop('-')  # we need to deal with hyphens
    punctuation = str.maketrans(p)
    weight_map = {}

    try:
        with open(file_name) as txt_file:
            body = txt_file.read().split(' ')
            body = list(filter(lambda t: t != '' and t != '-', body))  # remove single spaces and single hyphens

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


def init(directory, index):
    file_names = []  # Names of files
    chdir(directory)
    sorted_files = sorted(listdir(directory), key=lambda x: (int(re.sub('\D', '', x)), x))

    for file in sorted_files:
        if file.endswith('.txt'):
            file_names.append(str(file))

    # Index each file and mark its Document ID
    for file in file_names:
        index_file(file, int(re.findall(r'\d+', file)[0]), index)


def main():
    cwd = getcwd()
    start_time = time.time()
    # Federalist papers n shit
    all_files = '/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/ALL'
    # ------------------------------------------------------------------------------------------
    # Get rid of one things have been initialized
    init(all_files, all_docs_index)

    # i_writer = index_writer()
    # i_writer.write_index_to_disk(index.get_index())
    # ------------------------------------------------------------------------------------------
    jay_files = '/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/JAY'
    init(jay_files, jay_index)
    hamilton_files = '/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/HAMILTON'
    init(hamilton_files, hamilton_index)
    madison_files = '/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/MADISON'
    init(madison_files, madison_index)
    disputed_files = '/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/DISPUTED'
    init(disputed_files, disputed_index)
    chdir(cwd)  # come back to where the main is for the reading of files
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(jay_index.get_index())

    corpus_size = len(listdir(all_files))
    print("Corpus size of all federalist papers are {0}".format(corpus_size))

    # init(test_dir)
    print("--- %s seconds ---" % str((time.time() - start_time) / 60))

if __name__ == "__main__":
    main()
