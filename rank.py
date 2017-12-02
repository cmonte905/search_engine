from disk_inverted_index import disk_inverted_index

from math import log
from heapq import heappush, heappop
from porter2stemmer import Porter2Stemmer

stemmer = Porter2Stemmer()


class rank:

    def get_rank(self, q, corpus_size):
        """
        Gets ranks?
        :param q: Query string
        :param corpus_size: N in Wqt = ln(1 - (N/Dft))
        :return:
        """
        result_list = []
        disk_reader = disk_inverted_index()
        print('Query: ', q)
        Ad = {}
        for t in q.split():
            postings = disk_reader.get_postings_from_disk(stemmer.stem(t.lower()))  # The words get stemmed and lowered
            Wqt = log(1 + (corpus_size / len(postings)))
            print('Term:', t, 'Wqt = ', Wqt)
            for p in postings:
                # Ad = 0  # Accumilator?
                Wdt = 1 + log(p.get_term_frequency())
                if p.get_document_id() not in Ad:
                    Ad[p.get_document_id()] = 0
                Ad[p.get_document_id()] = Ad[p.get_document_id()] + (Wdt * Wqt)
        inverse_Ad = {}
        for a in Ad:
            ld = disk_reader.read_ld(a)  # Gets the Ld from disk
            Ad[a] = Ad[a] / ld  # Changes the accumulator to be (Σ Wqt*Wdt)/Ld for each document
            # print('The value after calcuations', Ad[a])\
            inverse_Ad[Ad[a]] = a
            heappush(result_list, (Ad[a] * -1))  # Fucking python only has min heap, not max heap
        first_ten = self.get_first_ten(result_list)
        for i in first_ten:
            print('Doc:', inverse_Ad[i], '| rank: ', i)
        return first_ten

    def get_first_ten(self, heap):
        result_list = []
        for i in range(10):
            result_list.append(-1 * heappop(heap))  # Again, fucking python uses min heap, so this happened
            if not heap:
                return result_list
        return result_list
