from KGramIndex import KGramIndex

class wildcard:

    def wildcard_parser(self, word):
        temp = '$' + word + '$'
        temp = temp.split('*')
        s = ''
        for t in temp:
            s += t
        return s 
   