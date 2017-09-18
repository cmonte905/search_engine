from jsonreader import read_corpus
def main():
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


