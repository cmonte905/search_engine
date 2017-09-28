import os.path
import json
import string
from positional_inverted_index import positional_inverted_index
from posting import posting
from kgram_index import kgram_index
from wildcard import wildcard

# Porter 2 Stemmer
from porter2stemmer import Porter2Stemmer
from query_parser import input_parser, wildcard_parser

# The Index
index = positional_inverted_index()

# List of vocab for terms in the corpus
vocab = {}

# Maps out terms with positions in the document into a dictionary
# {term : [positions]}
# returns a dictionary of terms and a list of it positions 
def find_positions(term_list):
    positions_dict = {}
    for i in range(0, len(term_list)):
        if (not term_list[i] in positions_dict):
            positions_dict[term_list[i]] = [i]
        else:
            positions_dict[term_list[i]].append(i)
    return positions_dict

# Use this index_file for .json files
def index_file(file_name, documentID):
    stemmer = Porter2Stemmer()
    punctuation = str.maketrans(dict.fromkeys(string.punctuation))
    with open(file_name) as json_file:
        article_data = json.load(json_file)
        
        body = (article_data['body']).lower().translate(punctuation).split(' ')
        body = list(filter(lambda w : w != '', map(lambda s : s.strip(), body)))

        term_positions = find_positions(body)

        for key in term_positions:
            index.add_term(key, documentID, term_positions[key])
            stemmed_term = stemmer.stem(key)
            if (stemmed_term != key and not stemmed_term in index.m_index):
                index.add_term(stemmer.stem(key), documentID, term_positions[key])

# If the user selects a certain document, for displaying the original content
def open_file_content(file_name):
    with open(file_name) as json_file:
        article_data = json.load(json_file)
        print (article_data['title'] + '\n')
        print (article_data['body'] + '\n')
        print (article_data['url'] + '\n')

def vocab():
    print (index.get_dictionary())
    print ('Term Count: ' + str(index.get_term_count()))

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
                            # TODO: ask neal
                            doc_list.append(post1.get_document_id())

    return doc_list

def create_kgram(self, word, k):
    kgram = []
    for i in range(0, len(word)):
        # starts at position i
        if i + k > len(word):
            break
                
        kgram.append(word[i: i + k])
    return kgram

# Testing of Kgrams
def k_gram_test(term):
    k = k_gram_index()
    for i in range(1, 4):
        k.add_string(term, i)
    print (k.get_kgrams())
    return k.get_kgrams()

def main():
    file_names = [] # Names of files
    documentID = 0  # Document ID

    k_list = {}

    # Testing KGram
    kgram = kgram_index()
    kgram.add_string('hello', 3)
    kgram.get_kgrams()


    w = wildcard()
    w.wildcard_parser('antidisestablishmentarianism')
    w.print_dict()


    # Find all .json files in this directory
    directory = os.path.dirname(os.path.realpath(__file__))
    for file in os.listdir(directory):
        if file.endswith('.json'):
            file_names.append(str(file))
    
    # Index each file and mark its Document ID
    for file in file_names:
        index_file(file, documentID)
        documentID = documentID + 1
        
    #vocab()

    '''
    while 1:
        user_string = input("Please enter a word search:\n")
        if ':' in user_string:
            print (user_string)
            if ':q' in user_string:
                exit()
            if ':stem' in user_string:
                print ("Will be stemming the token")
                print (user_string.split(" ")[1])
            if ':index' in user_string:
                print ('Will be indexing folder')
            if ':vocab' in user_string:
                print ('Will be spitting out words')
        elif '*' in user_string:
            print("This will get sent of to the wildcard class")
            wildcard_parser(user_string)
        else:
            input_parser(user_string)
            postings = get_postings(user_string)
            if len(postings) > 0:
                for id in postings:
                    ('document' + str(id))
    '''

    #print out the postings for each term in corpus
    #print (list(corpus_dict.keys())[0:20])

    # Dictionary alphabetized, prints terms only
    # print (index.get_dictionary())
    # Print each term and postings with it
    #for key in index.get_index():
        #index.print_term_info(key)

# Testing NEAR
    # use only with moby dick files for now
    # print(near('sand', 'massacre', 10))

    #print_term_info('whale')

# K Gram test
    #for term in index.get_index():
        #k_gram_test(term)

if __name__ == "__main__":
   	main()