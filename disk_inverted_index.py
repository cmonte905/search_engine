from porter2stemmer import Porter2Stemmer
from pos_db import position_db
from struct import unpack
from posting import posting

stemmer = Porter2Stemmer()

class disk_inverted_index:
    """
    m_path
    m_vocab_list
    m_postings
    m_vocab_table
    """

    def read_with_pos(self, term):
        position_term_db = position_db('/Users/Cemo/Documents/cecs429/search_engine/DB/disk_test1.db')
        # print('Position that is getting stored in DB for your:', position_term_db.get_term('your')[0])
        # print('Position that is getting stored in DB for you:', position_term_db.get_term('you')[0])

        t = stemmer.stem(term)
        file_loc = int(hex(position_term_db.get_term(t)[0]), 16)

        read_index_bin = open('index.bin', 'rb')

        print('File location:', file_loc)
        read_index_bin.seek(file_loc)
        raw_df = read_index_bin.read(4)
        # print('Raw DF from file: ', raw_df)
        dec_df = int.from_bytes(raw_df, byteorder='big')
        vocab_list_pos = [dec_df]  # Adds the doc freq.
        for i in range(dec_df):

            if i == 0:
                converted_doc_id = int.from_bytes(read_index_bin.read(4), byteorder='big')
            else:
                converted_doc_id = converted_doc_id + int.from_bytes(read_index_bin.read(4), byteorder='big')
            vocab_list_pos.append(converted_doc_id)
            converted_tf = int.from_bytes(read_index_bin.read(4), byteorder='big')
            # print('TF: ', converted_tf)
            vocab_list_pos.append(converted_tf)  # Adds the term freq.
            for j in range(converted_tf):
                if j == 0:
                    converted_pos = int.from_bytes(read_index_bin.read(4), byteorder='big')
                else:
                    converted_pos = converted_pos + int.from_bytes(read_index_bin.read(4), byteorder='big')
                vocab_list_pos.append(converted_pos)  # Adds the position
        read_index_bin.close()
        position_term_db.close_connection()
        return vocab_list_pos

    def read_without_pos(self, term):
        position_term_db = position_db('/Users/Cemo/Documents/cecs429/search_engine/DB/disk_test1.db')
        t = stemmer.stem(term)
        file_loc = int(hex(position_term_db.get_term(t)[0]), 16)

        read_index_bin = open('/Users/Cemo/Documents/cecs429/search_engine/index.bin', 'rb')
        read_index_bin.seek(file_loc)
        raw_df = read_index_bin.read(4)

        dec_df = int.from_bytes(raw_df, byteorder='big')  # Convert from bytes to int
        vocab_list_without_pos = [dec_df]  # DF of term in the list
        for i in range(dec_df):
            if i == 0:
                converted_doc_id = int.from_bytes(read_index_bin.read(4), byteorder='big')
            else:
                converted_doc_id = converted_doc_id + int.from_bytes(read_index_bin.read(4), byteorder='big')
            vocab_list_without_pos.append(converted_doc_id)  # Adds the doc id
            converted_tf = int.from_bytes(read_index_bin.read(4), byteorder='big')
            # print('TF: ', converted_tf)
            vocab_list_without_pos.append(converted_tf)  # Adds the tf
            for j in range(converted_tf):
                # Still reading these bytes to advanced the position of the file
                read_index_bin.read(4)

        read_index_bin.close()
        position_term_db.close_connection()
        return vocab_list_without_pos

    def read_ld(self, doc_id):
        weight_bin_file = open('/Users/Cemo/Documents/cecs429/search_engine/docWeights.bin', 'rb')
        weight_bin_file.seek(doc_id * 8 - 8)
        ld = weight_bin_file.read(8)
        readable_ld = unpack('d', ld)
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
        # print('\n\nPostings list before postings:', p_list)
        counter = 0
        df = p_list[counter]
        counter += 1
        for i in range(df):
            doc_id = p_list[counter]
            counter += 1
            # print('Doc id:', doc_id)
            tf = p_list[counter]
            # print('Tf i guess', tf)
            counter += 1
            pos_list = p_list[counter:tf+counter]
            counter += tf
            postings_list.append(posting(doc_id, pos_list))
        print(postings_list)
        return postings_list


    def get_postings_from_disk(self, term):
        print('These dont have any positions?')
        postings_list = []
        p_list = self.read_without_pos(term)
        counter = 0
        df = p_list[counter]
        counter += 1
        for i in range(df):
            doc_id = p_list[counter]
            counter += 1
            tf = p_list[counter]
            counter += 1
            pos_list = p_list[counter:tf + counter]
            counter += tf
            postings_list.append(posting(doc_id, pos_list))
        print(postings_list)
        return postings_list
