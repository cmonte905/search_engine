
import os

corpus_dict = {}

from jsonreader import read_corpus
def main():
	# The inverted index
	index = []

	import os
	for file in os.listdir("/mydir"):
    	if file.endswith(".txt"):
        	print(os.path.join("/mydir", file))

	print ('Enter name of the directory you wish to index')

	user_input = input('Please enter something: ')

	q = str()
	if '\"' in user_input:
		q = user_input.split('\"')
		print (q)


	print (q)
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

if __name__ == "__main__":
   	main()

def input_parser(input):
	q = str()
	if '\"' in iput:
		q = var.split('\"')
		print (q)

# NaiveInvertedIndex---------------------------------------------------------

# corpus_dict at the top of page

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
		print (key)
		terms.append(key)
	
	terms.sort()
	return terms

