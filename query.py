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
        """

        posting_lists = []
        query_list = []

        sub_list = list(findall(r'"([^"]*)"', user_string))
        user_string = sub(r'"([^"]*)"', " ", user_string)
        query_list.append(sub_list)  # Added in the phrase literal
        # Removes spaces at the end of strings
        query_list.append(split(r'\s+', user_string.lower().rstrip().lstrip()))

        print(query_list)
        if query_list[1]:  # For one word queries, gets info from postings
            posting_lists.append(self.query_process(query_list[1]))
        if query_list[0]:  # For Phrase queries
            self.double_quotes_process(query_list[0])
        return posting_lists

    def query_process(self, strings_list):
        temp = []

        stemmer = Porter2Stemmer()
        for s in strings_list:
            if stemmer.stem(s) in self.postings:
                print("Word that we are looking for:\n", stemmer.stem(s))
                for t in self.postings[stemmer.stem(s)]:
                    temp.append(int(t.get_document_id()))
            else:
                print("Word", s, "not in the index")
        temp = list(set(temp))
        temp.sort()
        return temp

    def double_quotes_process(self, strings_list):
        for s in strings_list:
            print(s)

