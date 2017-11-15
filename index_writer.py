from struct import pack
from pos_db import position_db
from VBE import vbe
from porter2stemmer import Porter2Stemmer

class index_writer():

    def write_index_to_disk(self, index):
        """
        Writes to disk whatever index dictionary that is given, slow as hell though
        :param index: Index gets passed a dictionary
        :return:
        """
        stem = Porter2Stemmer()
        vb = vbe()
        position_term_db = position_db('/Users/Cemo/Documents/cecs429/search_engine/DB/term_positions.db')
        position_term_db.create_table()
        current_index = index
        sorted_key_list = sorted(index)
        index_binary_file = open('index.bin', 'wb')

        for key in sorted_key_list:
            if not key:
                continue
            position_term_db.add_term(stem.stem(key.lower()), index_binary_file.tell())

            disk_write_list = []
            df = len(current_index[key])
            for number in vb.encode_number(df):
                index_binary_file.write(pack(">B", number))

            postings = current_index[key]
            for i in range(len(current_index[key])):
                # TODO gaps seems to be working
                if i == 0:
                    doc_id = postings[i].get_document_id()
                else:
                    doc_id = postings[i].get_document_id() - postings[i-1].get_document_id()

                disk_write_list.append(doc_id)

                for number in vb.encode_number(doc_id):
                    index_binary_file.write(pack(">B", number))

                tf = postings[i].positions_list
                disk_write_list.append(len(tf))

                for number in vb.encode_number(len(tf)):
                    index_binary_file.write(pack(">B", number))
                for j in range(len(tf)):
                    # TODO gaps seems to be working
                    if j == 0:
                        disk_write_list.append(tf[j])
                        vb.encode_number(tf[j])
                        for number in vb.encode_number(tf[j]):
                            index_binary_file.write(pack(">B", number))

                    else:
                        disk_write_list.append(tf[j] - tf[j - 1])
                        for number in vb.encode_number(tf[j] - tf[j - 1]):
                            index_binary_file.write(pack(">B", number))
        position_term_db.close_connection_commit()
        index_binary_file.close()

    def write_ld(self, Ld):
        ld_doc = open('/Users/Cemo/Documents/cecs429/search_engine/docWeights.bin', 'ab')
        ld_doc.write(pack('d', Ld))
        ld_doc.close()
