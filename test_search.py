from os import path, chdir, listdir
import json
import string
import pprint
import re

# Custom Classes
from positional_inverted_index import positional_inverted_index
from posting import posting
from kgram_index import kgram_index
from wildcard import wildcard
from near import near

# Porter 2 Stemmer
from porter2stemmer import Porter2Stemmer

from query import Query



def test_wildcard():
	w = wildcard()
	wildcard_list = w.wildcard_parser('mass*cre')
	assert ['$mass', 'cre$'] == wildcard_list

def test_kgram():
	k = kgram_index()
	kgram_list = k.create_kgram('$mass$', 3)
	assert ['$ma','mas','ass','ss$'] == kgram_list

def test_andquery():
	h = {}
	l1 = [1, 2, 10, 15]
	l2 = [1, 10, 50]
	q = Query(h)
	and_list = q.and_list(l1, l2)
	assert [1, 10] == and_list

def test_near():
	h = {}
	n = near()
	h['scienc'] = [posting(1, [31])]
	h['park'] = [posting(1, [1 ,2, 6, 34, 41, 58, 100])]

	s = n.near(h, 'scienc', 'park', 3)

	assert {1} == s

def test_orquery():
	h = {}
	l1 = [1, 3, 4, 6, 10]
	l2 = [1, 6, 15, 50]
	q = Query(h)
	or_list = q.or_list(l1, l2)
	assert {1, 3, 4, 6, 10, 15, 50} == or_list

def index_txt_file():
    txt_index = positional_inverted_index()
    stemmer = Porter2Stemmer()
    k = kgram_index()

    file_names = []
    documentID = 1

    # Dealing with punctuation
    p = dict.fromkeys(string.punctuation)
    p.pop('-') # we need to deal with hyphens
    punctuation = str.maketrans(p)

    directory = path.dirname(path.realpath(__file__)) + '/unit_test_docs/'
    chdir(directory)

    for file in listdir(directory):
        if file.endswith('.txt'):
            file_names.append(str(file))

    for file in file_names:
        try:
            with open(file) as txt_file:

                content = txt_file.readlines();
                content = content[0].lower().translate(punctuation).split(' ')
                content = list(filter(lambda w: w != '', map(lambda s: s.strip(), content)))

                positions_dict = {}
                for i in range(0, len(content)):
                    if '-' in content[i]:

                        hyphened_word_parts = content[i].split('-')
                        hyphened_word = content[i].replace('-', '')
                        hyphened_word_parts.append(hyphened_word)

                        for word in hyphened_word_parts:
                            if word in positions_dict:
                                positions_dict[word].append(i)
                            else:
                                positions_dict[word] = [i]
                    else:

                        if content[i] in positions_dict:
                            positions_dict[content[i]].append(i)
                        else:
                            positions_dict[content[i]] = [i]


                for key in positions_dict:
                    txt_index.add_term(stemmer.stem(key), documentID, positions_dict[key])
        except FileNotFoundError as e:
            i = 0
            print(e)

        documentID = documentID + 1

    for key in txt_index.get_index():
        txt_index.print_term_info(key)

     

