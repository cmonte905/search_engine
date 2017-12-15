from os import chdir, listdir, getcwd
from math import log, sqrt, pow
import string
import re
import pprint

# Custom Classes
from positional_inverted_index import positional_inverted_index

# Porter 2 Stemmer
from porter2stemmer import Porter2Stemmer
import time

# The Index
# { index[term] : [<ID, [p1, p2,... pk]>, <ID, [p1, p2,... pk]>, ...] }
all_docs_index = positional_inverted_index()


doc_wdt = {}
ham_vector = {}
mad_vector = {}
jay_vector = {}
# List of vocab tokens for terms in the corpus
# Dictionary <String : Set<String>>

def index_file(file_name, documentID, index):
    stemmer = Porter2Stemmer()
    # Dealing with punctuation
    p = dict.fromkeys(string.punctuation)
    p.pop('-')  # we need to deal with hyphens
    weight_map = {}

    try:
        with open(file_name) as txt_file:
            body = txt_file.read().replace('\n', '').split(' ')
            # body = txt_file.read().split(' ')
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

    score_map = {}
    wdt = 0
    # Gets the Wdt's of the terms in the file
    for tf in weight_map:
        score = pow(1 + log(weight_map[tf]), 2)
        score_map[tf] = score
        wdt += score**2
    Ld = sqrt(wdt)
    length = 0
    for tf in score_map:
        score_map[tf] = score_map[tf]/Ld
        length += score_map[tf]**2

    doc_wdt[file_name] = score_map
    # Things to turn in for Neal
    if file_name == 'paper_52.txt':
        print('First 30 components of document 52')
        get_first_thirty(score_map, True)


def train_rocchio(class_list, docs, name):
    if name == 'hamilton':
        vec = ham_vector
    elif name == 'madison':
        vec = mad_vector
    else:
        vec = jay_vector

    for i in docs:
        if i in class_list:
            inner_map = docs[i]
            for j in inner_map:
                if j not in vec:
                    vec[j] = inner_map[j]
                else:
                    vec[j] = vec[j] + inner_map[j]

    for i in vec:
        vec[i] = vec[i]/len(class_list)
    print('\nFirst thirty values of centroid {}'. format(name))
    get_first_thirty(vec, True)


def apply_rocchio(disputed_file):
    scores = [0.0, 0.0, 0.0]  # Hamilton, Madison, and Jay respectively
    disputed_index = doc_wdt[disputed_file]

    sum_vec = 0.0
    for i in disputed_index:
        if i in ham_vector:
            sum_vec += pow(ham_vector[i] - disputed_index[i], 2)
        else:
            sum_vec += pow(disputed_index[i], 2)
    scores[0] = sqrt(sum_vec)
    sum_vec = 0.0
    for i in disputed_index:
        if i in mad_vector:
            sum_vec += pow(mad_vector[i] - disputed_index[i], 2)
        else:
            sum_vec += pow(disputed_index[i], 2)
    scores[1] = sqrt(sum_vec)
    sum_vec = 0.0
    for i in disputed_index:
        if i in jay_vector:
            sum_vec += pow(jay_vector[i] - disputed_index[i], 2)
        else:
            sum_vec += pow(disputed_index[i], 2)
    scores[2] = sqrt(sum_vec)

    if disputed_file == 'paper_52.txt':
        print('Euclidians distance between the normalized vector for the document and each of the 3 class centroids')
        print('Hamilton {0} | Madison {1} | Jay {2}'.format(scores[0], scores[1], scores[2]))

    if scores[0] < scores[1] and scores[0] < scores[2]:
        print('{0} was written by Hamilton'.format(disputed_file))
    elif scores[1] < scores[0] and scores[1] < scores[2]:
        print('{0} was written by Madison'.format(disputed_file))
    else:
        print('{0} was written by Jay'.format(disputed_file))


def get_first_thirty(index, values=False):
    """
    Gets the first thirty words in the vocabulary for turn in
    :param index: A map to use to print out
    :param values: Option to print values if needed
    """
    counter = 1
    for i, j in sorted(index.items()):
        if counter <= 30 and values:
            print(counter, i, ':', j)
        elif counter <= 30:
            print(counter, i)
        counter += 1

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
    # Federalist papers n shit
    all_files = '/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/ALL'
    init(all_files, all_docs_index)

    jay_files = get_list_files('/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/JAY')
    hamilton_files = get_list_files('/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/HAMILTON')
    madison_files = get_list_files('/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/MADISON')
    disputed_files = get_list_files('/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/DISPUTED')

    print('First thirty terms in the index')
    get_first_thirty(all_docs_index.get_index())

    train_rocchio(hamilton_files, doc_wdt, 'hamilton')
    train_rocchio(madison_files, doc_wdt, 'madison')
    train_rocchio(jay_files, doc_wdt, 'jay')

    for i in disputed_files:
        apply_rocchio(i)


if __name__ == "__main__":
    main()
