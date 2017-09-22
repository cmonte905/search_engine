from sys import exit
import re

def input_parser(user_string):
    """
    First checks to see if there is a colon in the user's input and 
    runs the appropiate commands 
    """
    if ':' in user_string:
        print (user_string)
        if ':q' in user_string:
            exit()
        if ':stem' in user_string:
            print ("Will be stemming the token")
        if ':index' in user_string:
            print ('Will be indexing folder')
        if ':vocab' in user_string:
            print ('Will be spitting out words')
