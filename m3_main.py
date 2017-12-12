from os import chdir, listdir, getcwd
from math import log, sqrt, pow
import string
import re
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
# hamilton_index = positional_inverted_index()
# madison_index = positional_inverted_index()

doc_wdt = {}
ham_vector = {}
mad_vector = {}
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

    for tf in weight_map:
        weight_map[tf] = weight_map[tf]/Ld

    doc_wdt[file_name] = weight_map
    # i_writer.write_ld(Ld)


def train_rocchio(class_list, docs, name):
    if name == 'hamilton':
        vec = ham_vector
    else:
        vec = mad_vector
    for i in docs:
        if i in class_list:
            inner_map = docs[i]
            # print(name, ': ', i)
            for j in inner_map:
                if j not in vec:
                    vec[j] = inner_map[j]
                else:
                    vec[j] = vec[j] + inner_map[j]

    for i in vec:
        vec[i] = vec[i]/len(class_list)


def apply_rocchio(disputed_file):
    scores = [0.0, 0.0]  # Hamilton and Madison respectively
    disputed_index = doc_wdt[disputed_file]

    sum_vec = 0.0
    for i in disputed_index:
        if i in ham_vector and (ham_vector[i] - disputed_index[i]) >= 0:
            sum_vec += pow(ham_vector[i] - disputed_index[i], 2)
    scores[0] = sqrt(sum_vec)

    sum_vec = 0.0
    for i in disputed_index:
        if i in mad_vector and (mad_vector[i] - disputed_index[i]) >= 0:
            sum_vec += pow(ham_vector[i] - disputed_index[i], 2)
    scores[1] = sqrt(sum_vec)
    print('File name:', disputed_file, scores)
    pass


def get_list_files(directory):
    file_names = []  # Names of files
    chdir(directory)
    sorted_files = sorted(listdir(directory), key=lambda x: (int(re.sub('\D', '', x)), x))
    for file in sorted_files:
        if file.endswith('.txt'):
            file_names.append(str(file))
    return file_names


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
    jay_files = get_list_files('/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/JAY')
    hamilton_files = get_list_files('/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/HAMILTON')
    madison_files = get_list_files('/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/MADISON')

    disputed_files = get_list_files('/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/DISPUTED')

    chdir(cwd)  # come back to where the main is for the reading of files

    train_rocchio(hamilton_files, doc_wdt, 'hamilton')
    train_rocchio(madison_files, doc_wdt, 'madison')
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(ham_vector)
    # pp.pprint(mad_vector)
    for i in disputed_files:
        apply_rocchio(i)

    corpus_size = len(listdir(all_files))
    print("Corpus size of all federalist papers are {0}".format(corpus_size))

    # init(test_dir)
    print("--- %s seconds ---" % str((time.time() - start_time) / 60))

if __name__ == "__main__":
    main()
