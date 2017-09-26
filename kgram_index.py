class kgram_index:
	def __init__(self):
		self.k_gram_index = []
	
	def add_string(self, word, k):
		word = list('$' + word + '$')
		temp = ''
		#new_k_gram = []

		for i in range(0, len(word)):
			temp = word[i]
			#print (temp)

			# starts at position i
			if i + k <= len(word):
				for j in range(i + 1, i + k):
					temp += word[j]
			else:
				break

			self.k_gram_index.append(temp)

	def print_index(self):
		s = ''
		print (len(self.k_gram_index))
		for i in range(0, len(self.k_gram_index)):
			s += self.k_gram_index[i] + ' '

		print (s)

'''
Example of code to run this class
k = KGramIndex.KGramIndex()
k.add_string('hello', 3)
k.print_index()
'''



$hello$
$h
h
e
l
o


$h
el
lo
o$


$he
ell
llo
lo$


