class posting:
    def __init__(self, _id, pos_list):
        self.document_id = _id
        self.positions_list = pos_list

    def add_position(self, position):
        self.positions_list.append(position)

    def get_document_id(self):
        return str(self.document_id)
    
    def get_positions(self):
        return self.positions_list

    def print_posting(self):
        return str(str(self.document_id) + ' ' + str(self.positions_list))