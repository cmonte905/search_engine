
from re import sub, findall, split


class QueryParser:

    def input_parser(self, user_string):
        """
        First checks to see if there is a colon in the user's input and
        runs the appropiate commands
        """
        query_list = []
        sub_list = list(findall(r'"([^"]*)"', user_string))
        user_string = sub(r'"([^"]*)"', " ", user_string)
        query_list.append(sub_list)  # Added in the phrase literal
        query_list.append(split(r'\s+', user_string.rstrip()))  # Removes spaces at the end of the string
        print('Parsed out query list:\n', query_list)

    def double_quotes(self, strings):
        print(strings)
