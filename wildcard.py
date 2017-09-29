class wildcard:

	# Splits wildcard appends and prepends $ to word
    def wildcard_parser(self, word):
        temp = '$' + word + '$'
        temp = temp.split('*')
        return temp