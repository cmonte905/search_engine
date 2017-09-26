import os.path
import json
import string
# Porter 2 Stemmer
from porter2stemmer import Porter2Stemmer

# Binary Tree implementation
from binarytree import tree, pprint, convert

# The Index
corpus_dict = {}

# Custom Classes ----------------------------------------------------------------------------------

# Class to encapsulate one term posting
class posting:
    def __init__(self, _id, pos_list):
        self.document_id = _id
        self.positions_list = pos_list

    def add_position(position):
        self.positions_list.append(position)

    def get_document_id(self):
        return str(self.document_id)
    
    def get_positions(self):
        return self.positions_list

    def print_posting(self):
        return str(str(self.document_id) + ' ' + str(self.positions_list))

# Cutsom Methods ----------------------------------------------------------------------------------
def has_next_token(current_index, this_list):
    return (current_index < len(this_list) - 1)

def add_term(term, documentID, position):
    if (not term in corpus_dict):
        term_posting = posting(documentID, position)
        corpus_dict[term] = [term_posting]
    else:
        term_posting = posting(documentID, position)
        corpus_dict[term].append(term_posting)

# Maps out terms with positions in the document into a dictionary
# returns a dictionary of terms and a list of it positions 
def find_positions(term_list):
    positions_dict = {}
    for i in range(0, len(term_list)):
        if (not term_list[i] in positions_dict):
            positions_dict[term_list[i]] = [i]
        else:
            positions_dict[term_list[i]].append(i)
    return positions_dict

def term_count():
	return len(corpus_dict)

def get_postings(term):
	if (term in corpus_dict):
		return corpus_dict[term]
	return []

# Returns an alphabetized list of keys in corpus_dict
def get_dictionary():
    terms = list(corpus_dict.keys())
    terms.sort()
    return terms

# Use index_file for .txt files
'''
def index_file(file_name, documentID):
    stemmer = Porter2Stemmer()
    punctuation = str.maketrans(dict.fromkeys(string.punctuation))
    with open(file_name) as text_file:
        file_lines = []

        for line in text_file.readlines():
            line = line.lower().translate(punctuation)
            line_list = line.split(' ')

            for term in line_list:
                file_lines.append(term)

        # remove \n and ''
        file_lines = list(map(lambda s : s.strip(), file_lines))
        file_lines = list(filter(lambda s : s != '', file_lines))

        # Here we have a list of all terms as they appear in the text
        term_positions = find_positions(file_lines)

        # create postings for term
        for key in term_positions:
            add_term(key, documentID, term_positions[key])
            if (stemmer.stem(key) != key):
                add_term(stemmer.stem(key), documentID, term_positions[key])
'''
# Use this index_file for .json files
def index_file(file_name, documentID):
    stemmer = Porter2Stemmer()
    punctuation = str.maketrans(dict.fromkeys(string.punctuation))
    with open(file_name) as json_file:
        article_data = json.load(json_file)
        
        body = (article_data['body']).lower().translate(punctuation).split(' ')
        body = list(map(lambda s : s.strip(), body))
        body = list(filter(lambda s : s != '', body))

        term_positions = find_positions(body)

        for key in term_positions:
            add_term(key, documentID, term_positions[key])
            if (stemmer.stem(key) != key):
                add_term(stemmer.stem(key), documentID, term_positions[key])

def print_term_info(term):
    for post in corpus_dict[term]:
        print ('<' + term + ', [ID: ' + str(post.get_document_id()) + ' ' + str(post.get_positions()) + ']>')  

# k: how many terms away is first_term from second_term
# still need to be added
# - working with same words for frist and second term
def near(first_term, second_term, k):
    # query: first_term NEAR/k second_term
    # corpus_dict[term] : [<ID, [p1, p2,... pk]>, <ID, [p1, p2,... pk]>, ...]

    # list of documents that have first_term NEAR/k second_term
    doc_list = []
    
    for post1 in corpus_dict[first_term]:
        for post2 in corpus_dict[second_term]:
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

    #print out the postings for each term in corpus
    #print (list(corpus_dict.keys())[0:20])

# Dictionary alphabetized, prints terms only
    print (get_dictionary())

# Binary Tree test
    #term_tree = convert((get_dictionary())[50:65])
    #pprint(term_tree)

# Print each term and postings with it
    for key in corpus_dict:
        print_term_info(key)

# Tesing NEAR
    # use only with moby dick files for now
    #print(near('some', 'some', 8))

    #print_term_info('whale')

if __name__ == "__main__":
   	main()