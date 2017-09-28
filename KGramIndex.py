class KGramIndex:
	
	def create_kgram(self, word, k):
		kgram = []
		for i in range(0, len(word)):
			# starts at position i
			if i + k > len(word):
				break
				
			kgram.append(word[i: i + k])
		return kgram