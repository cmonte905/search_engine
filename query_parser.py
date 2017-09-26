from sys import exit
import re


def input_parser(user_string):
    """
    First checks to see if there is a colon in the user's input and
    runs the appropiate commands
    """
    query_list = []
    sub_list = list(re.findall(r'"([^"]*)"', user_string))
    user_string = re.sub(r'"([^"]*)"', " ", user_string)
    # print('User string after clean up:\n', user_string)
    query_list.append(sub_list)  # Added in the phrase literal
    query_list.append(re.split(r'\s+', user_string.rstrip()))  # Removes spaces at the end of the string
    print('Parsed out query list:\n', query_list)


def double_quotes(strings):
    print(strings)


def wildcard_parser(wildcard_string):
    print(wildcard_string)
