from posting import posting

class positional_inverted_index:

    def __init__(self):
        self.m_index = {}

    def get_index(self):
        return self.m_index
    
    # Add a term into the index
    def add_term(self, term, documentID, position):
        if (term in self.m_index):
            term_posting = posting(documentID, position)
            self.m_index[term].append(term_posting)
        else:
            term_posting = posting(documentID, position)
            self.m_index[term] = [term_posting]

    # Access the list of postings for a term
    def get_postings(self, term):
        if (term in self.m_index):
            return self.m_index[term]
        return []

    # Return a list of alphabetized keys of index
    def get_dictionary(self):
        terms = list(self.m_index.keys())
        terms.sort()
        return terms