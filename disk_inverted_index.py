from porter2stemmer import Porter2Stemmer
from pos_db import position_db

stemmer = Porter2Stemmer()

class disk_inverted_index:
    """
    m_path
    m_vocab_list
    m_postings
    m_vocab_table
    """

    def read_with_pos(self, term):
        position_term_db = position_db('/Users/Cemo/Documents/cecs429/search_engine/DB/disk_test.db')
        # print('Position that is getting stored in DB for your:', position_term_db.get_term('your')[0])
        # print('Position that is getting stored in DB for you:', position_term_db.get_term('you')[0])

        t = stemmer.stem(term)
        file_loc = int(hex(position_term_db.get_term(t)[0]), 16)

        read_index_bin = open('index.bin', 'rb')

        print('File location:', file_loc)
        read_index_bin.seek(file_loc)
        raw_df = read_index_bin.read(4)
        print('Raw DF from file: ', raw_df)
        dec_df = int.from_bytes(raw_df, byteorder='big')
        vl_pos = [dec_df]
        for i in range(dec_df):

            if i == 0:
                converted_doc_id = int.from_bytes(read_index_bin.read(4), byteorder='big')
            else:
                converted_doc_id = converted_doc_id + int.from_bytes(read_index_bin.read(4), byteorder='big')
            # print('Doc ID: ', converted_doc_id)
            vl_pos.append(converted_doc_id)
            converted_tf = int.from_bytes(read_index_bin.read(4), byteorder='big')
            # print('TF: ', converted_tf)
            vl_pos.append(converted_tf)
            for j in range(converted_tf):
                if j == 0:
                    converted_pos = int.from_bytes(read_index_bin.read(4), byteorder='big')
                else:
                    converted_pos = converted_pos + int.from_bytes(read_index_bin.read(4), byteorder='big')
                # print('Position ', j, ':', converted_pos)
                vl_pos.append(converted_pos)
        print('List with pos for baseball', vl_pos)
        read_index_bin.close()
        position_term_db.close_connection()
        return vl_pos

    def read_without_pos(self, term):
        position_term_db = position_db('/Users/Cemo/Documents/cecs429/search_engine/DB/disk_test.db')
        t = stemmer.stem(term)
        file_loc = int(hex(position_term_db.get_term(t)[0]), 16)

        read_index_bin = open('index.bin', 'rb')

        print('File location:', file_loc)
        read_index_bin.seek(file_loc)
        raw_df = read_index_bin.read(4)
        print('Raw DF from file: ', raw_df)

        dec_df = int.from_bytes(raw_df, byteorder='big')
        vl_without_pos = [dec_df]
        for i in range(dec_df):
            if i == 0:
                converted_doc_id = int.from_bytes(read_index_bin.read(4), byteorder='big')
            else:
                converted_doc_id = converted_doc_id + int.from_bytes(read_index_bin.read(4), byteorder='big')
            # print('Doc ID: ', converted_doc_id)
            vl_without_pos.append(converted_doc_id)
            converted_tf = int.from_bytes(read_index_bin.read(4), byteorder='big')
            # print('TF: ', converted_tf)
            vl_without_pos.append(converted_tf)
            for j in range(converted_tf):
                # Still reading these bytes to advanced the position of the file
                read_index_bin.read(4)
        print('List without pos for baseball:', vl_without_pos)

        read_index_bin.close()
        position_term_db.close_connection()
        return vl_without_pos


    def get_term_count(self):
        return len(self.m_vocab_table) / 2