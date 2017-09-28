# Only responsible for creating kgram based on input received

class kgram_index:
	def __init__(self):
		#self.k_gram_index = []
		self.vocab = {}

	# Creates the kgram tokens
	def add_string(self, word, k):
		k_gram_index = []
		temp = ''
		#new_k_gram = []
		for i in range(0, len(word)):
			temp = word[i]
			# starts at position i
			if i + k <= len(word):
				for j in range(i + 1, i + k):
					temp += word[j]
			else:
				break
			k_gram_index.append(temp)
		return k_gram_index


	def print_index(self):
		s = ''
		print (len(self.k_gram_index))
		for i in range(0, len(self.k_gram_index)):
			s += self.k_gram_index[i] + ' '
		print (s)

	def get_kgrams(self):
		return self.k_gram_index

	def reset(self):
		self.k_gram_index = []