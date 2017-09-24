import os
import string

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

# Cutsom Medthos ----------------------------------------------------------------------------------

def has_next_token(current_index, this_list):
    return (current_index < len(this_list) - 1)

def add_term(term, documentID, position):
    if (not term in corpus_dict):
        term_posting = posting(documentID, position)
        corpus_dict[term] = [term_posting]
    else:
    #elif (term in corpus_dict):
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

def get_dictionary():
	terms = []
	for key in corpus_dict.keys():
		terms.append(key)	
	terms.sort()
	return terms



def index_file(file_name, documentID):
    with open(file_name) as text_file:
        m_file_lines = []
        punctuation = str.maketrans(dict.fromkeys(string.punctuation))

        file_content = text_file.readlines()
        for line in file_content[0:]:
            line = line.lower().translate(punctuation)
            line_list = line.split(' ')

            for term in line_list:
                m_file_lines.append(term)

        # remove \n and ''
        m_file_lines = list(map(lambda s : s.strip(), m_file_lines))
        m_file_lines = list(filter(lambda s : s != '', m_file_lines))

        # Here we have a list of all terms as they appear in the text
                
        term_positions = find_positions(m_file_lines)
        for k in term_positions:
            print (k, term_positions[k])

        # create postings for term
        for key in term_positions:
            add_term(key, documentID, term_positions[key])
        for key in corpus_dict:
            print_term_info(key)

def print_term_info(term):
    for post in corpus_dict[term]:
        print ('<' + term + ', [ ID: ' + str(post.get_document_id()) + ' ' + str(post.get_positions()) + ']>')  

# k: how many terms away is first_term from second_term
def near(first_term, second_term, k):
    # first_term NEAR/k second_term
    # corpus_dict[term] : [<ID, [p1, p2,... pk]>, <ID, [p1, p2,... pk]>, ...]
    first_term_postings = corpus_dict[first_term]
    second_term_postings = corpus_dict[second_term]
    doc_list = []
    
    for post1 in first_term_postings:
        for post2 in second_term_postings:
            # if the doc ID's are the same, check this document
            if (post1.get_document_id() == post2.get_document_id()):
                for positions1 in post1.get_positions():
                    for positions2 in post2.get_positions():
                        if (abs(positions1 - positions2) <= k): 
                            doc_list.append(post1.get_document_id())

    return doc_list

def main():
    file_names = [] # Names of files
    documentID = 1

    directory = os.path.dirname(os.path.realpath(__file__))
    for file in os.listdir(directory):
        if file.endswith('.txt'):
            file_names.append(str(file))
    
    for file in file_names:
        index_file(file, documentID)
        documentID = documentID + 1

    print(near('bottom', 'sea', 3))

if __name__ == "__main__":
   	main()