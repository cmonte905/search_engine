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

	    count = 0

	    # Max number of iterations is the max size of the bigger list
	    max_length = max(len(index.get_postings(first_term)), len(index.get_postings(second_term)))

	    f_postings_list = index.get_postings(first_term)
	    s_postings_list = index.get_postings(second_term)
	    i = 0
	    j = 0

	    # Find matching doc ids
	    # compare doc ids, and increment the lower doc id[]

	    f_doc_ids = list(map(lambda p : p.get_document_id(), index.get_postings(first_term)))
	    s_doc_ids = list(map(lambda p : p.get_document_id(), index.get_postings(second_term)))

	    # the maximum number of times to iterate is the max length of the list
	    for n in range(0, max_length):
	    	if f_postings_list[i].get_document_id() == s_postings_list[j].get_document_id():
	    		f_pos_list = f_postings_list[i].get_positions()
	    		s_pos_list = s_postings_list[j].get_positions()

	    		# for any position that is less that the first list, get rid of it since its in order
	    		s_pos_list = list(filter(lambda p : p > f_pos_list[0], s_pos_list))

	    		#max_poslist_size = max(f_pos_list, s_pos_list)

	    		# second_pos - first_pos
	    		# we an return true for the first instance of true near
	    		for second_pos in s_pos_list:
	    			# find the distances between second word and first
	    			distances = list(map(lambda first_pos : second_pos - first_pos, f_pos_list))
	    			# change to true false if the distance was within k
	    			close_list = list(map(lambda p : p <= k, distances))
	    			if True in close_list:
	    				doc_list.add(f_postings_list[i].get_document_id())
	    				break

	    	# increment as needed
	    	i += int((f_postings_list[i].get_document_id() < s_postings_list[j].get_document_id()))
	    	j += int((f_postings_list[i].get_document_id() > s_postings_list[j].get_document_id()))


	    for post_1 in index[first_term]:
	        for post_2 in index[second_term]:
	            # if the doc ID's are the same, check that document
	            if (post_1.get_document_id() == post_2.get_document_id()):
	                for positions_1 in post_1.get_positions():
	                    for positions_2 in post_2.get_positions():
	                        #print (str(post_1.get_document_id()) + ' ' + str(abs(positions_2 - positions_1)))
	                        if (positions_2 - positions_1 <= k and (positions_2 > positions_1)):
	                            doc_list.add(post_1.get_document_id())
	    return doc_list

# science near/2 park