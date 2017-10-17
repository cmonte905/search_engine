# Class to encapsulate a single posting
class posting:
    def __init__(self, _id, pos_list):
        self.document_id = _id
        self.positions_list = pos_list

    def __str__(self):
        return 'doc_id: {0} : num of positions {1}'.format(self.document_id, len(self.positions_list))

    # print("a={0},b={1}".format(a, b))

    # Add a position to a postings list of postions
    def add_position(self, position):
        self.positions_list.append(position)

    # Return the document ID of a posting
    def get_document_id(self):
        return int(self.document_id)
    
    # Return a list of positions in a posting
    def get_positions(self):
        return self.positions_list

    # Print the information in a posting
    def print_posting(self):
        return str(str(self.document_id) + ' ' + str(self.positions_list))