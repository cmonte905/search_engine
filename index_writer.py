from struct import pack
from pos_db import position_db


class index_writer():

    def write_to_disk(self, index):
        """
        Writes to disk whatever index dictionary that is given, slow as hell though
        :param index: Index gets passed a dictionary
        :return:
        """
        position_term_db = position_db('/Users/Cemo/Documents/cecs429/search_engine/DB/disk_test.db')
        position_term_db.create_table()
        current_index = index
        sorted_key_list = sorted(index)

        index_binary_file = open('index.bin', 'wb')
        # print('Using the tell method on an empty file: ', index_binary_file.tell())

        for key in sorted_key_list:
            # print('Using the tell method, non byte:', index_binary_file.tell())
            position_term_db.add_term(key, index_binary_file.tell())
            disk_write_list = []
            df = len(current_index[key])
            # print('Using the tell method, using pack method for file pos.:', pack('>I', index_binary_file.tell()))
            # print('DF in dec: ', df)
            # print('DF in dec using pack: ', pack('>I', df))
            index_binary_file.write(pack('>I', df))
            # print('Pack value', pack('>I', df))
            # print('Non Packed value', df)
            # print('Position that is getting stored in DB:', position_term_db.get_term(key)[0])
            # print('Position that is getting stored in DB, using unpack:', unpack('I', position_term_db.get_term(key)[0]))
            # print('Position that is getting stored in DB:', position_term_db.get_term(key))
            # print('Using the tell method on a file that has something written to it: ', index_binary_file.tell())

            disk_write_list.append(df)

            # print('Key:', key, '| DF', df)  # No need to gaps this
            postings = current_index[key]
            for i in range(len(current_index[key])):
                # TODO gaps seems to be working
                if i == 0:
                    doc_id = postings[i].get_document_id()
                else:
                    doc_id = postings[i].get_document_id() - doc_id

                disk_write_list.append(doc_id)

                index_binary_file.write(pack('>I', doc_id))

                tf = postings[i].positions_list

                disk_write_list.append(len(tf))

                index_binary_file.write(pack('>I', len(tf)))
                # print('Key:', key, '| doc id:', doc_id)
                # print('TF: ', len(tf))  # No need to gaps this shit either
                for j in range(len(tf)):
                    # TODO gaps seems to be working
                    if j == 0:
                        disk_write_list.append(tf[j])
                        index_binary_file.write(pack('>I', tf[j]))
                    else:
                        disk_write_list.append(tf[j] - tf[j - 1])
                        index_binary_file.write(pack('>I', tf[j - 1]))
                        # print('Position p:', tf[j])

        position_term_db.print_db()
        position_term_db.close_connection()
        index_binary_file.close()
