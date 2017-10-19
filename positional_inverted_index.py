from posting import posting

# Class for storing all functionality of a working index
class positional_inverted_index:

    # Constuctor for positional_inverted_index
    def __init__(self):
        self.m_index = {}

    def get_index(self):
        return self.m_index
    
    # Add a term into the index
    def add_term(self, term, documentID, position):
        # if the term already exists in the index
        if (term in self.m_index):
            # if there is already a posting with that docID, add the position to the end
            if self.m_index[term][-1].get_document_id() == documentID:
                self.m_index[term][-1].get_positions().append(position)
            # if not, add a new posting to it
            else:
                term_posting = posting(documentID, [position])
                self.m_index[term].append(term_posting)
        else:
            term_posting = posting(documentID, [position])
            self.m_index[term] = [term_posting]

    # Access the list of postings for a term
    def get_postings(self, term):
        if (term in self.m_index):
            return self.m_index[term]
        return []
        #return self.m_index[term] if (term in self.m_index) else []

    # Return a list of alphabetized keys of index
    def get_dictionary(self):
        terms = list(self.m_index.keys())
        terms.sort()
        return terms

    # return how many terms are in the index
    def get_term_count(self):
        return len(self.m_index)

    # Prints out all the postings of a key
    def print_term_info(self, term):
        for post in self.m_index[term]:
            print ('<' + term + ', [ID: ' + str(post.get_document_id()) + ' ' + str(post.get_positions()) + ']>') 

    def clean(self):
        self.m_index = {}

    def get_all_doc_ids(self, term):
        #return list(map(lambda posting : posting.get_document_id(), self.m_index.get_postings(term)))

        id_list = set()
        for post in self.m_index[term]:
            id_list.add(post.get_document_id())

        return id_list