
from re import sub, findall, split


class Query:
    posting_lists = []
    query_list = []


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

        if query_list[0]:  #
            self.double_quotes_process(query_list[0])
        if query_list[1]:
            self.query_process(query_list[1])

        return posting_lists

    def query_process(self, string_list):
        print(string_list)


    def double_quotes_process(self, strings):
        print(strings)
