from re import sub, findall, split
from porter2stemmer import Porter2Stemmer
import pprint

pp = pprint.PrettyPrinter(indent=4)
stemmer = Porter2Stemmer()


class Query:

    def __init__(self, postings):
        self.postings = postings
        self.q_dict = {}

    def plus_parse(self, string):
        return string.split('+')

    def phrase_parse(self, string):
        return string.lower().rstrip().lstrip().replace(' ', '-')

    def clean_space(self, string):
        return string.split(r'\s+', string.lower().rstrip().lstrip())

    def query_parser(self, user_string):
        """
        First checks to see if there is a colon in the user's input and
        runs the appropiate commands
        """
        sub_list = list(findall(r'"([^"]*)"', user_string))
        user_string = sub(r'"([^"]*)"', "!", user_string)
        temp_list = []
        for s in sub_list:
            temp_list.append(self.phrase_parse(s))

        temp_string = ''
        for s in user_string:
            if s == '!':
                temp_string += temp_list[0].lstrip().rstrip()
                temp = temp_list.pop(0)
            else:
                temp_string += s
        query_list = self.plus_parse(temp_string)

        or_list = []
        for s in query_list:
            temp_results_list = []
            for t in s.split(' '):
                if t:  # if not empty
                    if '-' in t:
                        temp_results_list.append(self.phrase_process(t.lower()))
                    else:
                        temp_results_list.append(self.query_process(t.lower()))
            if len(temp_results_list) == 1:  # if only one thing got parsed, then just added it to or list
                temp = list(set(temp_results_list[0]))
                temp.sort()
                or_list.append(temp)
            else:  # Have to and the result if there are two or more things in temp results list
                anded_lists = temp_results_list[0]
                for i in range(len(temp_results_list) - 1):
                    anded_lists = self.and_list(anded_lists, temp_results_list[i + 1])
                or_list.append(anded_lists)
        if len(or_list) == 1:  # If only one thing in it, returns its first element
            return or_list[0]
        else:
            results_lists = or_list[0]
            for i in range(len(or_list) - 1):
                results_lists = list(self.or_list(results_lists, or_list[i +1]))
            results_lists.sort()
            return results_lists


    def query_process(self, string):
        temp_list = []
        if stemmer.stem(string) in self.postings:
            for t in self.postings[stemmer.stem(string)]:  # adds doc id to a temporary list
                temp_list.append(int(t.get_document_id()))
        else:
            print("Word", string, "not in the index")
        temp_list.sort
        return temp_list

    def phrase_process(self, strings):  # Testing -> Prairie National, Site Indentification
        doc_list = []
        parsed_q = strings.split('-')

        for i in range(len(parsed_q) - 1):
            doc_list = set()
            # stemming words first, can remove this later
            first_term = stemmer.stem(parsed_q[i])
            second_term = stemmer.stem(parsed_q[i+1])

            if first_term in self.postings and second_term in self.postings:
                for post_1 in self.postings[first_term]:
                    for post_2 in self.postings[second_term]:
                        # if the doc ID's are the same, check that document
                        if post_1.get_document_id() == post_2.get_document_id():
                            for positions_1 in post_1.get_positions():
                                for positions_2 in post_2.get_positions():
                                    if abs(positions_2 - positions_1) <= i+1:
                                        doc_list.add(int(post_1.get_document_id()))
                                    else:
                                        if post_1 in doc_list:
                                            doc_list.remove(post_1.get_document_id())
            else:
                print('Phrase', strings, 'not found')
                return []
        # Python is funny with its sorting of lists, has to be done this way
        return_list = list(doc_list)
        return_list.sort()
        return list(return_list)

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