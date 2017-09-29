class KGramIndex:
	# Will iterate through the word to 
	# create the kgrams of size k
	def create_kgram(self, word, k):
		kgram = []
		for i in range(0, len(word)):
			if i + k > len(word):
				break
			kgram.append(word[i : i + k])
		return kgram