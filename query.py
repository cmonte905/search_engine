from re import sub, findall, split
from porter2stemmer import Porter2Stemmer
import pprint

pp = pprint.PrettyPrinter(indent=4)
stemmer = Porter2Stemmer()


class Query:

    def __init__(self, postings):
        self.index = postings
        self.postings = postings.get_index()

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
        string_parsed = strings.split('-')
        doc_list = set()
        stemmer = Porter2Stemmer()

        for k in range(len(string_parsed) - 1):
            # stemming words first, can remove this later
            first_term = stemmer.stem(string_parsed[k])
            second_term = stemmer.stem(string_parsed[k+1])

            # Max number of iterations is the max size of the bigger list
            # max_length = max(len(index.get_postings(first_term)), len(index.get_postings(second_term)))

            f_postings_list = self.index.get_postings(first_term)
            s_postings_list = self.index.get_postings(second_term)
            i = 0
            j = 0

            # both_set = index.get_all_doc_ids(first_term).intersection(index.get_all_doc_ids(second_term))
            # the maximum number of times to iterate is the max length of the list
            while 1:
                if i + 1 >= len(f_postings_list) or j + 1 >= len(s_postings_list):
                    return_list = list(doc_list)
                    return return_list

                if f_postings_list[i].get_document_id() == s_postings_list[j].get_document_id():
                    f_pos_list = f_postings_list[i].get_positions()
                    s_pos_list = s_postings_list[j].get_positions()

                    # for any position that is less that the first list, get rid of it
                    # the only positions that matter are second positions after the first pos
                    s_pos_list = list(filter(lambda p: p > f_pos_list[0], s_pos_list))

                    # second_pos - first_pos
                    # we an return true for the first instance of true near

                    for second_pos in s_pos_list:
                        # find the distances between second word and first
                        distances = list(
                            map(lambda first_pos: ((second_pos - first_pos <= i + 1) and second_pos > first_pos), f_pos_list))
                        if any(list(map(lambda p: p <= i + 1, distances))):
                            doc_list.add(f_postings_list[i].get_document_id())
                            break
                        else:
                            doc_list.remove(f_postings_list[i].get_document_id())
                    i += 1
                    j += 1

                else:
                    # increment as needed
                    i += int((f_postings_list[i].get_document_id() < s_postings_list[j].get_document_id()))
                    j += int((f_postings_list[i].get_document_id() > s_postings_list[j].get_document_id()))


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

