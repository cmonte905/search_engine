
import os.path
import string
import sys
from jsonreader import read_corpus

corpus_dict = {}

# Things i needed -----------------------------------------------------------------------------------------------------

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
    print ('Files in this directory: ')
    directory = os.path.dirname(os.path.realpath(__file__))

    # names of the files
    file_names = []
    documentID = 0

    # loops through the current directory and find all .txt files
    for file in os.listdir(directory):
        # files that end with .txt
        if file.endswith('.txt'):
            # print each file
            #print(os.path.join(directory, file))
            dir_path = os.path.join(directory, file).split('\\')
            file_names.append(dir_path[-1])

    # for each of the files in file_name
    for file in file_names:
        # open the file and parse it
        with open(file) as text_file:
            m_file_lines = []
            remover = str.maketrans('', '', string.punctuation)

            # read each line
            file_content = text_file.readlines()
            for line in file_content[0:]:
                # remove punctuation and lowercase everything
                line = line.lower().translate(remover)
                # split each word by spaces
                line_list = line.split(' ')

                # add each term to m_file_lines
                for term in line_list:
                    m_file_lines.append(term)

            # remove \n and ''
            m_file_lines = list(map(lambda s : s.strip(), m_file_lines))
            m_file_lines = list(filter(lambda s : s != '', m_file_lines))

            index = 0
            while (has_next_token(index, m_file_lines)):
                # fix this
                add_term(m_file_lines[index], documentID)
                index = index + 1

            documentID = documentID + 1
    # print (m_file_lines)
    # print (corpus_dict)

    # get_dictionary()

    print_results()

    # User input
    while True:
        command = input('Please enter a term would you like to search: ')
        if (command == 'quit'):
            print ('Bye!')
            sys.exit
        else:
            print ('These documents contain that term: ')
            postings = get_postings(command)
            if (len(postings) > 0):
                for id in postings:
                    print ('document' + str(id))

if __name__ == "__main__":
   	main()

'''
	while 1:
		print('Quit (:q) Stem (:stem) Index (:index) Vocab (:vocab)')
		user_input = input('Please enter something: ')

		if user_input == ":q":
			print('Quitting...')
			break
		elif user_input == ":stem":
			print('Stemming')
		elif user_input == ":index":
			print('Indexing')
		elif user_input == ":vocab":
			print('Vocab')
		else:
			print('No special query')

	print('Ended')
'''

def input_parser(input):
	q = str()
	if '\"' in iput:
		q = var.split('\"')
		print (q)