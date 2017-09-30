from re import sub, findall, split
from porter2stemmer import Porter2Stemmer
from posting import posting
import pprint

pp = pprint.PrettyPrinter(indent=4)
stemmer = Porter2Stemmer()

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
        query_list.append(split(r'\s+', user_string.rstrip().lstrip()))  # Removes spaces at the end of the string
        if query_list[0]:  # For Phrase queries
            self.double_quotes_process(query_list[0])
        if query_list[1]:  # For one word queries
            posting_lists.append(self.query_process(query_list[1]))

        return posting_lists

    def query_process(self, strings_list):
        for s in strings_list:
            if s.lower() in self.postings:
                print("Word that we are looking for", s)
                print(self.postings[stemmer.stem(s.lower())])
                for t in self.postings[s.lower()]:
                    temp = []
                    temp.append(t.get_document_id())
                    print('Document id of : ', int(t.get_document_id()))
                return temp
            else:
                print("Word", s, "not in the index")

    def double_quotes_process(self, strings_list):
        for s in strings_list:
            print(s)
