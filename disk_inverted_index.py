from porter2stemmer import Porter2Stemmer
from pos_db import position_db
from struct import unpack
from posting import posting, positionless_postings
from VBE import vbe

stemmer = Porter2Stemmer()


class disk_inverted_index:

    def read_with_pos(self, term, pos=True):
        """
        Reads in the positions from disk in binary
        :param term:
        :param pos:
        :return: List of integers that will be converted into postings
        """
        vb = vbe()
        position_term_db = position_db('/Users/Cemo/Documents/cecs429/search_engine/DB/term_positions.db')
        t = stemmer.stem(term.lower())
        file_loc = int(hex(position_term_db.get_term(t)[0]), 16)

        read_index_bin = open('index.bin', 'rb')
        read_index_bin.seek(file_loc)
        # raw_df = read_index_bin.read(4)
        df = vb.decode(self.readFromFile(read_index_bin))[0]
        # dec_df = int.from_bytes(raw_df, byteorder='big')
        vocab_list_pos = [df]  # Adds the doc freq.
        for i in range(df):
            if i == 0:
                # converted_doc_id = int.from_bytes(read_index_bin.read(4), byteorder='big')
                converted_doc_id = vb.decode(self.readFromFile(read_index_bin))[0]
            else:
                # converted_doc_id = converted_doc_id + int.from_bytes(read_index_bin.read(4), byteorder='big')
                converted_doc_id = converted_doc_id + vb.decode(self.readFromFile(read_index_bin))[0]
            vocab_list_pos.append(converted_doc_id)
            # converted_tf = int.from_bytes(read_index_bin.read(4), byteorder='big')
            converted_tf = vb.decode(self.readFromFile(read_index_bin))[0]
            vocab_list_pos.append(converted_tf)  # Adds the term freq.
            if pos:
                for j in range(converted_tf):
                    if j == 0:
                        # converted_pos = int.from_bytes(read_index_bin.read(4), byteorder='big')
                        converted_pos = vb.decode(self.readFromFile(read_index_bin))[0]
                    else:
                        # converted_pos = converted_pos + int.from_bytes(read_index_bin.read(4), byteorder='big')
                        converted_pos = converted_pos + vb.decode(self.readFromFile(read_index_bin))[0]
                    vocab_list_pos.append(converted_pos)  # Adds the position
            else:
                counter = 0
                while counter < converted_tf:
                    if unpack('>B', bytearray(read_index_bin.read(1)))[0] > 127:
                        counter += 1

        read_index_bin.close()
        position_term_db.close_connection()
        return vocab_list_pos

    def readFromFile(self, bin_file):
        """
        Reads from file VBE
        :param bin_file:
        :return:
        """
        result = []
        n = unpack('>B', bytearray(bin_file.read(1)))[0]  # Unpack gives a tuple, just want the first things
        result.append(n)
        while n < 128:
            n = unpack('>B', bytearray(bin_file.read(1)))[0]
            result.append(n)
        return result

    def read_ld(self, doc_id):
        """
        Gets the document weight for a given document
        :param doc_id: Document id
        :return: The ld of a document in a readable format
        """
        weight_bin_file = open('/Users/Cemo/Documents/cecs429/search_engine/docWeights.bin', 'rb')
        weight_bin_file.seek(doc_id * 8 - 8)
        ld = weight_bin_file.read(8)
        readable_ld = unpack('d', ld)
        weight_bin_file.close()
        return readable_ld[0]

    def get_pos_postings_from_disk(self, term):
        """
        Assume that the term will get stemmed from main, not here
        :param term:
        :return: Array of postings? Maybe a one thing dict with the term and postings for the values, or just return
        the list and have a dict outside of this that will take care of that
        """
        postings_list = []
        p_list = self.read_with_pos(term)
        counter = 0
        df = p_list[counter]
        counter += 1
        for i in range(df):
            doc_id = p_list[counter]
            counter += 1
            tf = p_list[counter]
            counter += 1
            pos_list = p_list[counter:tf+counter]
            counter += tf
            postings_list.append(posting(doc_id, pos_list))
        return postings_list

    def get_postings_from_disk(self, term):
        """
        Assume that the term will get stemmed from main, not here. Use counters instead of for inner for loops
        to make things less slow
        :param term:
        :return: Array of positionless postings, postings that have doc_id and tf but no positions
        """
        postings_list = []
        p_list = self.read_with_pos(term, False)
        counter = 0
        df = p_list[counter]
        counter += 1
        for i in range(df):
            doc_id = p_list[counter]
            counter += 1
            tf = p_list[counter]
            counter += 1
            postings_list.append(positionless_postings(doc_id, tf))
        return postings_list
