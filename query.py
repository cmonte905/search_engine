from re import sub, findall, split
from porter2stemmer import Porter2Stemmer
import pprint

pp = pprint.PrettyPrinter(indent=4)


class Query:
    def __init__(self, postings):
        self.postings = postings

    def query_parser(self, user_string):
        """
        First checks to see if there is a colon in the user's input and
        runs the appropiate commands
        List of lists being created, first list has all the phrase queries
        second list has the rest of queries, seperate the list with
        """

        # posting_lists = []
        query_list = []

        sub_list = list(findall(r'"([^"]*)"', user_string))
        user_string = sub(r'"([^"]*)"', " ", user_string)
        query_list.append(sub_list)  # Added in the phrase literal
        # Removes spaces at the end of strings
        query_list.append(split(r'\s+', user_string.lower().rstrip().lstrip()))

        print(query_list)
        if not len(query_list[1]) == 0:  # For one word queries, gets info from postings
            posting_lists = (self.query_process(query_list[1]))
        if not len(query_list[0]) == 0:  # For Phrase queries
            self.double_quotes_process(query_list[0])
        return posting_lists

    def query_process(self, strings_list):
        temp_list = []
        stemmer = Porter2Stemmer()

        print(strings_list)
        for s in strings_list:
            if stemmer.stem(s) in self.postings:
                for t in self.postings[stemmer.stem(s)]:
                    temp_list.append(int(t.get_document_id()))

            elif '+' in stemmer.stem(s):
                print('Printing for some reason', s)

            else:
                print("Word", s, "not in the index")

        # temp = list(set(temp_list))  # Gets rid of any duplicates within the list
        temp_list.sort()
        return temp_list

    def double_quotes_process(self, strings_list):
        for s in strings_list:
            for t in s.split(' '):
                print(t)

    def and_list(list1, list2):
        temp_list = []
        temp_num1 = 0
        temp_num2 = 0
        while True:
            if temp_num1 == len(list1) or temp_num2 == len(list2):
                return temp_list
            if list1[temp_num1] == list2[temp_num2]:
                print(list1[temp_num1], list2[temp_num2])
                temp_list.append(list1[temp_num1])
                temp_num1 += 1
                temp_num2 += 1
            else:
                if list1[temp_num1] < list2[temp_num2]:
                    temp_num1 += 1
                else:
                    temp_num2 += 1


'''
# still need to be added
def near(first_term, second_term, k):
    # query: first_term NEAR/k second_term
    # index[term] : [<ID, [p1, p2,... pk]>, <ID, [p1, p2,... pk]>, ...]

    # list of documents that have first_term NEAR/k second_term
    doc_list = []
    for post1 in index.get_index()[first_term]:
        for post2 in index.get_index()[second_term]:
            # if the doc ID's are the same, check that document
            if (post1.get_document_id() == post2.get_document_id()):
                for positions1 in post1.get_positions():
                    for positions2 in post2.get_positions():
                        distance = positions2 - positions1
                        # if (abs(distance) <= k):
                        if (distance <= k and not distance <= 0): 
                            # TODO: ask neal
                            doc_list.append(post1.get_document_id())
'''
