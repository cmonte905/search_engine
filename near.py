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

	    for post_1 in index[first_term]:
	        for post_2 in index[second_term]:
	            # if the doc ID's are the same, check that document
	            if (post_1.get_document_id() == post_2.get_document_id()):
	                for positions_1 in post_1.get_positions():
	                    for positions_2 in post_2.get_positions():
	                        print (str(post_1.get_document_id()) + ' ' + str(abs(positions_2 - positions_1)))
	                        if (positions_2 - positions_1 <= k):
	                            doc_list.add(post_1.get_document_id())
	    return doc_list

# science near/2 park