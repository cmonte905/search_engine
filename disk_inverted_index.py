class disk_inverted_index:
	'''
	m_path
	m_vocab_list
	m_postings
	m_vocab_table
	'''

	def __init__(self, path):
		try:
    		self.m_path = path
			self.m_vocab_list = open('something.txt', 'r')
			self.m_postings = open('something.txt', r)
			self.m_vocab_table = 
			#self.m_file_names =
    	except FileNotFoundError as ex:
	        i = 0
	        print(ex)

    def read_posting_from_file(self, postings, postings_position):
    	try:
    		posting.seek(postings_position)

    	except FileNotFoundError as ex:
	        i = 0
	        print(ex)


   	def get_postings(self, term):
