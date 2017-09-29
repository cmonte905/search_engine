from KGramIndex import KGramIndex

class wildcard:

    def wildcard_parser(self, word):
        temp = '$' + word + '$'
        temp = temp.split('*')
        s = ''
        for new_word in temp:
            s += new_word
        return s