import os.path
import string
import sys
from query_parser import input_parser, wildcard_parser

corpus_dict = {}


def has_next_token(current_index, this_list):
    # if the current index is less that the max index of the list, hasnext is true
    return (current_index < len(this_list) - 1)


# Naive Inverted Index ------------------------------------------------------------------------------------------------

# def add_term(term, documentID, position): # add this
def add_term(term, documentID):
    if (not term in corpus_dict):
        id_list = []
        id_list.append(documentID)
        corpus_dict[term] = id_list
    elif (term in corpus_dict and (not documentID in corpus_dict[term])):
        corpus_dict[term].append(documentID)


def term_count():
    return len(corpus_dict)


def get_postings(term):
    if (term in corpus_dict):
        return corpus_dict[term]
    return []


def get_dictionary():
    terms = []
    for key in corpus_dict.keys():
        # print (key)
        terms.append(key)

    terms.sort()
    return terms


# ---------------------------------------------------------------------------------------------------------------------

def print_results():
    t = get_dictionary()
    for term in t:
        print (term + ': ' + str(get_postings(term)))


# changes need to be made to parse the new corpus
# this strcitly works for testing the moby dick chapters
def main():
    
    file_names = [] # Names of files
    documentID = 0

    # Find all .txt files in this directory
    directory = os.path.dirname(os.path.realpath(__file__))
    for file in os.listdir(directory):
        if file.endswith('.json'):
        # if file.endswith('.txt'):
            file_names.append(str(file))
    
    # Index each file and mark its Document ID
    for file in file_names:
        index_file(file, documentID)
        documentID = documentID + 1


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


if __name__ == "__main__":
    main()

