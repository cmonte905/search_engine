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
from near import near

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

                index.add_term(stemmer.stem(key), documentID, term_positions[key])
    except FileNotFoundError as e:
        i = 0
        print(e)


# If the user selects a certain document, for displaying the original content
def open_file_content(file_name):
    with open(file_name, 'r') as json_file:
        article_data = json.load(json_file)
        print('_______________________________________________________________________________________________________')
        print(article_data['title'] + '\n')
        print (article_data['body'] + '\n')
        print (article_data['url'] + '\n')
        print('_______________________________________________________________________________________________________')

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

    interected_list = list(set(canidate_lists[0].intersection(*canidate_lists[1:])))

    n = list(map(lambda t : stemmer.stem(t), interected_list))
    n = list(map(lambda t : index.get_index()[t], n))

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
    # User input their own directory
    #directory = input('Enter directory for index: ')
    chdir(directory)
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


def main():
    

    # Instances
    w = wildcard()
    n = near()
    directory = input('Enter directory for index: ')
    start_time = time.time()
    init(directory)
    print("--- %s seconds ---" % str((time.time() - start_time) / 60))

    # Find all .json files in this directory
    # directory = path.dirname(path.realpath(__file__)) + '/corpus/all-nps-sites/'
    #directory = path.dirname(path.realpath(__file__))

    while 1:

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
        elif '*' in user_string:
            print("This will get sent of to the wildcard class")
            return_docs.extend(wild(user_string))
        elif 'near' in user_string:
            # Parse NEAR input
            near_parts = user_string.split(' ')
            k = near_parts[1].split('/')
            return_docs.extend(n.near(index.get_index(), near_parts[0], near_parts[2], int(k[1])))
        else:
            if user_string:
                q = Query(index.get_index())
                return_docs = q.query_parser(user_string)
                #for i in results_list:
                    #print('json' + str(i) + '.json')
                #print('Num of results:\n', len(results_list))
            else:
                print('No query entered')

        print ('DOC_LIST: ' + str(return_docs))

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
    
    

    # Print every token in vocab and the words that contain that token
    #for token in vocab:
    #    print (token, str(vocab[token]))


    # Print each term and postings with it
    #for key in index.get_index():
    #    index.print_term_info(key)


    # TEST: Wildcard and KGram tesing
    #wild('**acre')




if __name__ == "__main__":
    main()