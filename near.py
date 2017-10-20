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

        #print ('Input:  ' + str(stemmed_first_term) + ' ' + str(stemmed_second_term) + ' ' + str(k))

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
                    #print ('BROKEN')
                    if a >= len(f_pos_list) or b >= len(s_pos_list):
                        break

                    if (s_pos_list[b] > f_pos_list[a]) and (s_pos_list[b] - f_pos_list[a] <= k):
                        print (str(s_pos_list[b])  + ' - ' + str(f_pos_list[a]) + ' = ' + str(s_pos_list[b] - f_pos_list[a]) + ' <= ' + str(k))
                        doc_list.append(f_postings_list[i].get_document_id())
                        break
                        '''
                        if a < len(f_pos_list):
                            a += 1
                        if b < len(s_pos_list): 
                            b += 1
                        '''
                        #print ('a = ' + str(a) +  ' b = ' + str(b))
                    else:
                        a += int(f_pos_list[a] < s_pos_list[b])

                        #print ('A is now ' + str(a) + ' ' + str(a == len(f_pos_list)))

                        if a == len(f_pos_list):

                            #print ('A) ' + stemmed_first_term + ' ' + str(a) + ' and ' + stemmed_second_term + ' ' + str(b))

                            break
                        b += int(f_pos_list[a] > s_pos_list[b])

                        #print ('B is now ' + str(b) + ' ' + str(b == len(s_pos_list)))

                        if b == len(s_pos_list):

                            #print ('B) ' + stemmed_first_term + ' ' + str(a) + ' and ' + stemmed_second_term + ' ' + str(b))

                            break
                        '''
                        if a + 1 < len(f_pos_list) - 1:
                            a += int(f_pos_list[a] > s_pos_list[b])
                        if b + 1 < len(s_pos_list) - 1:
                            b += int(f_pos_list[a] < s_pos_list[b])
                        '''
                i += 1
                j += 1

            else:
                i += int((f_postings_list[i].get_document_id() < s_postings_list[j].get_document_id()))
                j += int((f_postings_list[i].get_document_id() > s_postings_list[j].get_document_id()))

        #doc_list = list(map(lambda d: 'json' + str(d) + '.json', list(doc_list)))

        return doc_list