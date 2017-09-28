from KGramIndex import KGramIndex

class wildcard:
    def __init__(self):
        self.k = kgram_index()
        self.vocab = {}

    def wildcard_parser(self, word):
        temp = '$' + word + '$'
        temp = temp.split('*')
        kg = []
        k_size = 0

        for i in range(0, len(temp)):
            if len(temp[i]) < 3:
                k = len(temp[i])
            else:
                k = 3
            kg.append(self.k.add_string(temp[i], k))
            self.k.reset()
        for i in range(0, len(kg)):
            t = kg[i]
            for j in range(0, len(t)):
                if t[j] in self.vocab.keys():
                    self.vocab[t[j]].append(word)
                else:
                    self.vocab[t[j]] = [word]

    def print_dict(self):
    	k = list(self.vocab.keys())
    	for i in range(0, len(k)):
    		print(k[i] + ' ' + str(len(self.vocab[k[i]])))
    	'''
        for key in self.vocab:
            k = self.vocab.keys()
            for j in range(0, len(k)):
                print(key + ' : ' + k[j])
                '''

    def get_dict(self):
    	return self.vocab