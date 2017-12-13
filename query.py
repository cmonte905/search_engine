from re import sub, findall
from porter2stemmer import Porter2Stemmer
from disk_inverted_index import disk_inverted_index
import pprint

pp = pprint.PrettyPrinter(indent=4)
stemmer = Porter2Stemmer()


class Query:
    """
    Got to fix this shit later, was too busy to do so
    """
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
                results_lists = list(self.or_list(results_lists, or_list[i + 1]))
            results_lists.sort()
            return results_lists


    def query_process(self, string):
        temp_list = []
        disk_reader = disk_inverted_index()
        postings = disk_reader.get_pos_postings_from_disk(stemmer.stem(string))

        for t in postings:  # adds doc id to a temporary list
            temp_list.append(int(t.get_document_id()))
        return temp_list

    def phrase_process(self, strings):  # Testing -> Prairie National, Site Indentification
        string_parsed = strings.split('-')
        disk_reader = disk_inverted_index()
        doc_list = []

        for k in range(len(string_parsed) - 1):  # Goes on for how long the phrase is
            # stemming words first, can remove this later
            current_list = []  # Empty in the beginning, used if phrase query is long, otherwise just one pass will do

            first_term = stemmer.stem(string_parsed[k])
            second_term = stemmer.stem(string_parsed[k+1])

            # Max number of iterations is the max size of the bigger list
            # max_length = max(len(index.get_postings(first_term)), len(index.get_postings(second_term)))
            if len(current_list) == 0:  # If first time going through, then first word will be our postings
                f_postings_list = disk_reader.get_pos_postings_from_disk(first_term)

            s_postings_list = disk_reader.get_pos_postings_from_disk(second_term)
            i = 0
            j = 0
            count = 1
            # both_set = index.get_all_doc_ids(first_term).intersection(index.get_all_doc_ids(second_term))
            # the maximum number of times to iterate is the max length of the list
            while 1:
                if i + 1 >= len(current_list) or j + 1 >= len(s_postings_list):
                    break
                if current_list[i].get_document_id() == s_postings_list[j].get_document_id():
                    f_pos_list = current_list[i].get_positions()
                    s_pos_list = s_postings_list[j].get_positions()
                    a = 0
                    b = 0
                    while 1:
                        if a >= len(f_pos_list) or b >= len(s_pos_list):
                            # Wanted to update the current list here but it is not the best place to do that
                            print('Supposed to get out', k)
                            break

                        if (s_pos_list[b] > f_pos_list[a]) and (s_pos_list[b] - f_pos_list[a] <= count):
                            doc_list.append(current_list[i].get_document_id())
                            print('If they are a match', k)
                            break

                        else:
                            print('If they do not match', k)
                            # If its false, then remove it from the list, make sure it is in the list first though
                            if current_list[i].get_document_id() in doc_list:
                                doc_list.remove(current_list[i].get_document_id())
                            a += int(f_pos_list[a] < s_pos_list[b])
                            if a == len(f_pos_list):
                               break
                            b += int(f_pos_list[a] > s_pos_list[b])
                            if b == len(s_pos_list):
                                break
                        i += 1
                        j += 1

                else:
                    i += int((current_list[i].get_document_id() < s_postings_list[j].get_document_id()))
                    j += int((current_list[i].get_document_id() > s_postings_list[j].get_document_id()))
            count += 1
        return doc_list

        #         if current_list[i].get_document_id() == s_postings_list[j].get_document_id():
        #             f_pos_list = current_list[i].get_positions()
        #             s_pos_list = s_postings_list[j].get_positions()
        #
        #             # for any position that is less that the first list, get rid of it
        #             # the only positions that matter are second positions after the first pos
        #             s_pos_list = list(filter(lambda p: p > f_pos_list[0], s_pos_list))
        #
        #             # second_pos - first_pos
        #             # we an return true for the first instance of true near
        #
        #             for second_pos in s_pos_list:
        #                 # find the distances between second word and first
        #                 distances = list(
        #                     map(lambda first_pos: ((second_pos - first_pos <= i + 1) and second_pos > first_pos), f_pos_list))
        #                 if any(list(map(lambda p: p <= i + 1, distances))):
        #                     doc_list.append(current_list[i].get_document_id())
        #                     break
        #                 else:
        #                     doc_list.remove(current_list[i].get_document_id())
        #             i += 1
        #             j += 1
        #
        #         else:
        #             # increment as needed
        #             i += int((current_list[i].get_document_id() < s_postings_list[j].get_document_id()))
        #             j += int((current_list[i].get_document_id() > s_postings_list[j].get_document_id()))
        #
        # return_list = list(doc_list)
        # return return_list
    # This dont work, plz dont look at me


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

    def phrase_current_list(self, post_list, current_doc_ids):
        """
        Gets 2(3?) lists, one of postings, one of doc ids, returns a list of postings back
        based on the doc ids that we got back
        :param post_list: list of postings from one of the words, shouldnt matter which list it is
        since we will be getting the same postings back anyways
        :param current_doc_ids: Doc ids current found from the previous phrase query
        :return: Current list, postings to use for the next word
        """
        return_list = []
        for i in post_list:
            if i.get_document_id() in current_doc_ids:
                return_list.append(i)

        return return_list
