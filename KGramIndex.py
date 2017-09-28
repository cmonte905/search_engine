class KGramIndex:
	def __init__(self):
		self.k_gram_index = []
		self.vocab = {}


	def add_string(self, word, k):
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
			self.k_gram_index.append(temp)
		return self.k_gram_index


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