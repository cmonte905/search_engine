from os import path, chdir, listdir
import json
import string
import pprint
import re

# Custom Classes
from positional_inverted_index import positional_inverted_index
from posting import posting
from kgram_index import kgram_index
from wildcard import wildcard

# Porter 2 Stemmer
from porter2stemmer import Porter2Stemmer

from query import Query

# The Index
# { index[term] : [<ID, [p1, p2,... pk]>, <ID, [p1, p2,... pk]>, ...] }
index = positional_inverted_index()

# List of vocab tokens for terms in the corpus
# Dictionary <String : Set<String>>
vocab = {}

pp = pprint.PrettyPrinter(indent=4)


# Maps out terms with positions in the document into a dictionary
# returns a dictionary of term keys and list of positions as value
# {term : [positions]}
def find_positions(term_list):
    positions_dict = {}
    for i in range(0, len(term_list)):

        # Hyphened words
        # Because they all share the same position when split
        if '-' in term_list[i]:

            hyphened_word_parts = term_list[i].split('-')
            hyphened_word = term_list[i].replace('-', '')
            hyphened_word_parts.append(hyphened_word)

            for word in hyphened_word_parts:
                if word in positions_dict:
                    positions_dict[word].append(i)
                else:
                    positions_dict[word] = [i]
        else:

            if term_list[i] in positions_dict:
                positions_dict[term_list[i]].append(i)
            else:
                positions_dict[term_list[i]] = [i]

    return positions_dict


# Use this index_file for .json files
def index_file(file_name, documentID):
    stemmer = Porter2Stemmer()
    k = kgram_index()
    # punctuation = str.maketrans(dict.fromkeys(string.punctuation))

    # Dealing with punctuation
    p = dict.fromkeys(string.punctuation)
    p.pop('-')  # we need to deal with hyphens
    punctuation = str.maketrans(p)

    try:
        with open(file_name) as json_file:
            article_data = json.load(json_file)

            body = (article_data['body']).lower().translate(punctuation).split(' ')
            body = list(filter(lambda w: w != '', map(lambda s: s.strip(), body)))

            term_positions = find_positions(body)

            for key in term_positions:

                # KGram stuff
                kgram_list = []

                # develop a list of kgram tokens for one specific term
                for i in range(1, 4):
                    if i is 1:
                        kgram_list.extend(k.create_kgram(key, i))
                    else:
                        s = ('$' + key + '$')
                        kgram_list.extend(k.create_kgram(s, i))

                # Shove each of those tokens into the grand vocab dictionary
                for token in kgram_list:
                    if token in vocab:
                        vocab[token].add(key)

                    else:
                        vocab[token] = set([key])

                '''
                # we shouldn't need this 
                for token in vocab:
                    if token in key:
                        vocab[token].append(key)
                '''

            for key in term_positions:
                # stemmed_term = stemmer.stem(key)
                # index.add_term(key, documentID, term_positions[key])
                index.add_term(stemmer.stem(key), documentID, term_positions[key])
                # if stemmed_term != key and not stemmed_term in index.m_index:
                # index.add_term(stemmed_term, documentID, term_positions[key])
    except FileNotFoundError as e:
        i = 0
        print(e)


# If the user selects a certain document, for displaying the original content
def open_file_content(file_name):
    with open(file_name, 'r') as json_file:
        article_data = json.load(json_file)
        print('________________________________________________________________________________________________')
        print(article_data['title'] + '\n')
        # print (article_data['body'] + '\n')
        # print (article_data['url'] + '\n')


def near(first_term, second_term, k):
    # query: first_term NEAR/k second_term
    # index[term] : [<ID, [p1, p2,... pk]>, <ID, [p1, p2,... pk]>, ...]
    # list of documents that have first_term NEAR/k second_term
    # post_list = [(post_1, post_2) for post_1 in index.get_index()[first_term] for post_2 in index.get_index()[second_term] if post_1.get_document_id() == post_2.get_document_id()]
    # return [(pos_1, pos_2) for pos_1 in post_1.get_positions() for pos_2 in post_2.get_positions() if (pos_2 - pos_1 <= k) and not (distance <= 0)]

    # doc_list = []
    doc_list = set()

    # stemming words first, can remove this later
    stemmer = Porter2Stemmer()
    first_term = stemmer.stem(first_term)
    second_term = stemmer.stem(second_term)

    for post_1 in index.get_index()[first_term]:
        for post_2 in index.get_index()[second_term]:
            # if the doc ID's are the same, check that document
            if (post_1.get_document_id() == post_2.get_document_id()):
                ID = post_1.get_document_id()
                for positions_1 in post_1.get_positions():
                    for positions_2 in post_2.get_positions():
                        distance = positions_2 - positions_1
                        # if (abs(distance) <= k):

                        # List way
                        # if (distance <= k and not distance <= 0 and not ID in doc_list):
                        #    doc_list.append(ID)

                        # Using a set for no duplicate docs ID's
                        if (distance <= k and not distance <= 0):
                            doc_list.add(ID)
    return doc_list


# Wild card input
# word_input: the user input of a wild card. 
# EX:   land*cape
#       he*lo
# 
def wild(word_input):
    kg = kgram_index()
    w = wildcard()

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

    print(ktokens)

    canidate_lists = []

    for token in ktokens:
        if token in vocab:
            canidate_lists.append(vocab[token])
            print(token, list(vocab[token]))

    print(set(canidate_lists[0]).intersection(*canidate_lists[1:]))

    return set(canidate_lists[0].intersection(*canidate_lists[1:]))


def main():
    file_names = []  # Names of files
    documentID = 0  # Document ID

    # Instances
    w = wildcard()

    # Find all .json files in this directory
    # directory = path.dirname(path.realpath(__file__)) + '/corpus/all-nps-sites/'
    directory = path.dirname(path.realpath(__file__))
    # chdir(directory)
    '''
    for file in listdir(directory):
        directory = path.dirname(os.path.realpath(__file__))
    print(directory)
    '''
    for file in listdir(directory):
        if file.endswith('.json'):
            file_names.append(str(file))

    # Index each file and mark its Document ID
    for file in file_names:
        index_file(file, re.findall(r'\d+', file)[0])
        # Print every token in vocab and the words that contain that token
        # for token in vocab:
        # print (token, str(vocab[token]))

    # for word in index.get_dictionary():
    #     w = ('$' + word + '$')
    #     for token in vocab:
    #         if token in w:
    #             vocab[token].append(word)

    # for token in vocab:
    #     print (token, str(vocab[token]))


    # Wildcard and Kgram tesing
    # wild('**acre')

    '''
    while 1:
        first = raw_input('Enter first word: ')
        second = raw_input('Enter second word: ')

        near()
    '''
    # vocab()



    while 1:

        user_string = input("Please enter a word search:\n")
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
            if ':vocab' in user_string:
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(index.get_dictionary())
                print(index.get_term_count())
                print('Will be spitting out words')
        elif '*' in user_string:
            print("This will get sent of to the wildcard class")
        else:
            q = Query(index.get_index())
            results_list = q.query_parser(user_string)
            for i in results_list:
                print('json' + str(i) + '.json')
            print('Num of results:\n', len(results_list))





                # Print all keys in index
                # print (index.get_dictionary())
                # Print all keys in index
                # print (index.get_dictionary())



                # Print each term and postings with it
                # for key in index.get_index():
                #   index.print_term_info(key)

                # Print each term and postings with it
                # for key in index.get_index():
                #     index.print_term_info(key)


                # Testing NEAR
                # stem word before doing it
                # print(near('sand', 'massacre', 10))


                # K Gram test
                # for term in index.get_index():
                # k_gram_test(term)


if __name__ == "__main__":
    main()
