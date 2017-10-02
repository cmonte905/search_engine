class wildcard:

	# Splits wildcard appends and prepends $ to word and
	# returns a list of the tokens
    def wildcard_parser(self, word):
        return ('$' + word + '$').split('*')