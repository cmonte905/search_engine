from os import path, chdir, listdir
import json
import string
import pprint
import re

# Custom Classes
from positional_inverted_index import positional_inverted_index
from posting import posting
from kgram_index import kgram_index

# Porter 2 Stemmer
from porter2stemmer import Porter2Stemmer
from query import Query

# The Index
# { index[term] : [<ID, [p1, p2,... pk]>, <ID, [p1, p2,... pk]>, ...] }
index = positional_inverted_index()

# List of vocab for terms in the corpus
vocab = {}

pp = pprint.PrettyPrinter(indent=4)


# Maps out terms with positions in the document into a dictionary
# {term : [positions]}
# returns a dictionary of term keys and list of positions as value
def find_positions(term_list):
    positions_dict = {}
    for i in range(0, len(term_list)):
        if term_list[i] in positions_dict:
            positions_dict[term_list[i]].append(i)
        else:
            positions_dict[term_list[i]] = [i]
    return positions_dict


# Use this index_file for .json files
def index_file(file_name, documentID):
    stemmer = Porter2Stemmer()
    punctuation = str.maketrans(dict.fromkeys(string.punctuation))
    try:
        with open(file_name) as json_file:
            article_data = json.load(json_file)

            body = (article_data['body']).lower().translate(punctuation).split(' ')
            body = list(filter(lambda w: w != '', map(lambda s: s.strip(), body)))

            term_positions = find_positions(body)

            for key in term_positions:

                # KGram stuff
                k = kgram_index()
                kgram_list = []

                # rip magic number, let it be por favor, jesus will forgive us
                for i in range(1, 4):
                    if i is 1:
                        kgram_list.extend(k.create_kgram(key, i))
                    else:
                        s = ('$' + key + '$')
                        kgram_list.extend(k.create_kgram(s, i))

                for token in kgram_list:
                    if token in vocab and not key in vocab[token]:
                        # vocab[token].append()
                        continue
                    else:
                        vocab[token] = []

                '''
                s = ('$' + key + '$')
                for token in vocab:
                    if token in s and not key in vocab[token]:
                        vocab[token].append(key)
                '''
                # print (kgram_list)


                stemmed_term = stemmer.stem(key)
                index.add_term(key, documentID, term_positions[key])
                if stemmed_term != key and not stemmed_term in index.m_index:
                    index.add_term(stemmed_term, documentID, term_positions[key])
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
    doc_list = []
    for post1 in index.get_index()[first_term]:
        for post2 in index.get_index()[second_term]:
            # if the doc ID's are the same, check that document
            if (post1.get_document_id() == post2.get_document_id()):
                for positions1 in post1.get_positions():
                    for positions2 in post2.get_positions():
                        distance = positions2 - positions1
                        # if (abs(distance) <= k):
                        if (distance <= k and not distance <= 0):
                            doc_list.append(post1.get_document_id())

    return doc_list


def main():
    file_names = []  # Names of files
    documentID = 0  # Document ID

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

    for word in index.get_dictionary():
        w = ('$' + word + '$')
        for token in vocab:
            if token in w:
                vocab[token].append(word)

    # for token in vocab:
    #     print (token, str(vocab[token]))



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
            q_list = q.query_parser(user_string)
            if not len(q_list) == 0:
                print('Postings list : ', q_list, '\n', len(q_list))
            else:
                print('There is no document matched your query')





            # Print all keys in index
            # print (index.get_dictionary())

            # print out the postings for each term in corpus
            # print (list(corpus_dict.keys())[0:20])

            # Print each term and postings with it
            # for key in index.get_index():
            #   index.print_term_info(key)

            # Testing NEAR
            # use only with moby dick files for now
            # print(near('sand', 'massacre', 10))

            # print_term_info('whale')

            # K Gram test
            # for term in index.get_index():
            # k_gram_test(term)


if __name__ == "__main__":
    main()
