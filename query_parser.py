from sys import exit
import re


def input_parser(user_string):
    """
    First checks to see if there is a colon in the user's input and 
    runs the appropiate commands 
    """

    # if ':' in user_string:
    #     print (user_string)
    #     if ':q' in user_string:
    #         exit()
    #     if ':stem' in user_string:
    #         print ("Will be stemming the token")
    #     if ':index' in user_string:
    #         print ('Will be indexing folder')
    #     if ':vocab' in user_string:
    #         print ('Will be spitting out words')

    query_list = re.findall(r'"([^"]*)"', user_string)
    user_string = re.sub(r'"([^"]*)"', " ", user_string)
    print(user_string)
    # print("User string after getting rid of white space:\n", re.split(r'\s+', user_string))
    # query_list.append(list(user_string.split(r'\s+')))
    # query_list = list(filter(lambda x: x != '', query_list))
    # print("User string, hopefully after getting the spaces removed:\n", user_string)
    # print('Query list', query_list)


def double_quotes(strings):
    print(strings)


def wildcard_parser(wildcard_string):
    print(wildcard_string)
