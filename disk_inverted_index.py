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

	# Reads and returns a list of document IDs that contain the given term.
   	def get_postings(self, term):
   		postings_position = self.binary_search_vocabulary(term)
   		if postings_position >= 0:
   			return read_posting_from_file(self.m_postings, postings_position)
   		return 0

   	# Locates the byte position of the postings for the given term.
   	def binary_search_vocabulary(term):
   		i = 0
   		j = len(self.m_vocab_table) / 2 - 1

   		while i <= j:
   			try:
   				m = (i + j) / 2
   				v_list_position = self.m_vocab_table[m * 2]
   				term_length = 0
   				if m == len(self.m_vocab_table) / 2 - 1:
   					term_length = int(len(self.m_vocab_list) - self.m_vocab_table[m * 2])
   				else:
   					term_length = int(m_vocab_table[(m + 1) * 2] - v_list_position)

   			self.m_vocab_list.seek(v_list_position)

   			mbuffer =  bytearray(term_length)
   			self.m_vocab_list.read(mbuffer, 0, len(mbuffer))

   			document_frequency = 0

   			doc_ids = [document_frequency]

   			except Exception as ex:
   				print(ex)


   	def read_vocab_table(index_name):
   		try:
   			table_file = open(index_name, 'r', 'vocabTable.bin')
   			
   			byte_buffer = bytearray(4)
   			table_file.read(byte_buffer, 0, len(byte_buffer))

   			table_index = 0

   			vocab_table = 

   		except Exception as e:
   			print (ex)

   	def get_term_count():
   		return len(self.m_vocab_table) / 2