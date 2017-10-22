from positional_inverted_index import positional_inverted_index
from posting import posting
from porter2stemmer import Porter2Stemmer

class near:
    def near(self, index, first_term, second_term, k):
        doc_list = []

        stemmer = Porter2Stemmer()
        stemmed_first_term = stemmer.stem(first_term).lower()
        stemmed_second_term = stemmer.stem(second_term).lower()

        f_postings_list = index.get_postings(stemmed_first_term)
        s_postings_list = index.get_postings(stemmed_second_term)

        i = 0
        j = 0
        while 1:
            if i >= len(f_postings_list) or j >= len(s_postings_list):
                return doc_list

            if f_postings_list[i].get_document_id() == s_postings_list[j].get_document_id():
                f_pos_list = f_postings_list[i].get_positions()
                s_pos_list = s_postings_list[j].get_positions()

                a = 0
                b = 0
                while 1: 
                    if a >= len(f_pos_list) or b >= len(s_pos_list):
                        break

                    if (s_pos_list[b] > f_pos_list[a]) and (s_pos_list[b] - f_pos_list[a] <= k):
                        print (str(s_pos_list[b])  + ' - ' + str(f_pos_list[a]) + ' = ' + str(s_pos_list[b] - f_pos_list[a]) + ' <= ' + str(k))
                        doc_list.append(f_postings_list[i].get_document_id())
                        break
                    else:
                        a += int(f_pos_list[a] < s_pos_list[b])
                        if a == len(f_pos_list):
                            break
                        b += int(f_pos_list[a] > s_pos_list[b])
                        if b == len(s_pos_list):
                            break
                i += 1
                j += 1

            else:
                i += int((f_postings_list[i].get_document_id() < s_postings_list[j].get_document_id()))
                j += int((f_postings_list[i].get_document_id() > s_postings_list[j].get_document_id()))

        return doc_list