from posting import posting

class positional_inverted_index:

    m_index = {}

    def __init__(self):


    def get_index():
        return m_index
    
    # Add a term into the index
    def add_term(term, documentID, position):
        if (not term in m_index):
            term_posting = posting(documentID, position)
            m_index[term] = [term_posting]
        else:
            term_posting = posting(documentID, position)
            m_index[term].append(term_posting)

    # Access the list of postings for a term
    def get_postings(term):
        if (term in m_index):
            return m_index[term]
        return []

    # Return a list of alphabetized keys of index
    def get_dictionary():
        terms = list(m_index.keys())
        terms.sort()
        return terms