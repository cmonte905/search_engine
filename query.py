from re import sub, findall, split
from porter2stemmer import Porter2Stemmer
import pprint

pp = pprint.PrettyPrinter(indent=4)

'''
w1 + w1 = w1 or w1
w1
'''


class Query:

    def __init__(self, postings):
        self.postings = postings
        self.q_dict = {}

    def query_parser(self, user_string):
        """
        First checks to see if there is a colon in the user's input and
        runs the appropiate commands
        """
        query_list = []

        sub_list = list(findall(r'"([^"]*)"', user_string))
        user_string = sub(r'"([^"]*)"', " ", user_string)
        query_list.append(sub_list)  # Added in the phrase literal
        # Removes spaces at the end of strings
        query_list.append(split(r'\s+', user_string.lower().rstrip().lstrip()))

        # print(query_list)
        if not len(query_list[1]) == 0:  # For non-phrase queries, gets info from postings
            posting_lists = (self.query_process(query_list[1]))
        if not len(query_list[0]) == 0:  # For Phrase queries
            self.phrase_process(query_list[0])
        print(posting_lists)
        return posting_lists

    def query_process(self, strings_list):

        stemmer = Porter2Stemmer()
        print(strings_list)

        for s in strings_list:
            temp_list = []
            if stemmer.stem(s) in self.postings:
                for t in self.postings[stemmer.stem(s)]:  # adds doc id to a temporary list
                    temp_list.append(int(t.get_document_id()))
            else:
                print("Word", s, "not in the index")

            self.q_dict[s] = list(set(temp_list))

        print('Value of q_dict', self.q_dict)
        anded_lists = self.q_dict[strings_list[0]]
        anded_lists.sort()
        for i in range(len(strings_list) - 1):
            print(i)
            print('List of ', strings_list[i], ':', self.q_dict[strings_list[i]])

            anded_lists = (self.and_list(anded_lists, self.q_dict[strings_list[i + 1]]))

        print('And list:', anded_lists)
        anded_lists.sort()
        return anded_lists

    def phrase_process(self, strings_list):
        for s in strings_list:
            for t in s.split(' '):
                print(t)

    def and_list(self, list1, list2):
        list1.sort()  # Sorted here cause it doesnt want to sort earlier before
        list2.sort()
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

    def or_list(self, list1, list2):
        temp = list1
        temp.extend(list2)
        return set(temp)