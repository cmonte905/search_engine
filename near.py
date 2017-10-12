from positional_inverted_index import positional_inverted_index
from posting import posting
from porter2stemmer import Porter2Stemmer

class near:
    def near(self, index, first_term, second_term, k):

        doc_list = set()

        # stemming words first, can remove this later
        stemmer = Porter2Stemmer()
        first_term = stemmer.stem(first_term)
        second_term = stemmer.stem(second_term)

        # Max number of iterations is the max size of the bigger list
        #max_length = max(len(index.get_postings(first_term)), len(index.get_postings(second_term)))

        f_postings_list = index.get_postings(first_term)
        s_postings_list = index.get_postings(second_term)
        i = 0
        j = 0

        #both_set = index.get_all_doc_ids(first_term).intersection(index.get_all_doc_ids(second_term))
        # the maximum number of times to iterate is the max length of the list
        while 1:
            if i + 1 >= len(f_postings_list) or j + 1 >= len(s_postings_list):
                return doc_list

            if f_postings_list[i].get_document_id() == s_postings_list[j].get_document_id():
                f_pos_list = f_postings_list[i].get_positions()
                s_pos_list = s_postings_list[j].get_positions()

                w, z = 0
                # for any position that is less that the first list, get rid of it
                # the only positions that matter are second positions after the first pos
                #s_pos_list = list(filter(lambda p : p > f_pos_list[0], s_pos_list))
                a, b = 0
                while 1: 
                	if a + 1 >= len(f_pos_list) or b + 1 >= len(s_pos_list):
                		break

                	if s_pos_list[b] - f_pos_list[a] <= k and (s_pos_list[b] > f_pos_list[a]):

                	a += f_pos_list[a] > s_pos_list[b]
                	b += f_pos_list[b] < s_pos_list[a]

                # second_pos - first_pos
                # we an return true for the first instance of true near

                for second_pos in s_pos_list:
                    # find the distances between second word and first
                    distances = list(map(lambda first_pos : ((second_pos - first_pos <= k) and second_pos > first_pos), f_pos_list))
                    if any(distances):
                        doc_list.add(f_postings_list[i].get_document_id())
                        break

                i += 1
                j += 1

            else:
                # increment as needed
                i += int((f_postings_list[i].get_document_id() < s_postings_list[j].get_document_id()))
                j += int((f_postings_list[i].get_document_id() > s_postings_list[j].get_document_id()))

        return doc_list

# science near/2 park