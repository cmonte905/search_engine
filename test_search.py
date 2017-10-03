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

def index_txt_file(file_name, documentID):
    stemmer = Porter2Stemmer()
    k = kgram_index()
    #punctuation = str.maketrans(dict.fromkeys(string.punctuation))

    # Dealing with punctuation
    p = dict.fromkeys(string.punctuation)
    p.pop('-') # we need to deal with hyphens
    punctuation = str.maketrans(p)

    try:
        with open(file_name) as txt_file:

            content = txt_file.readlines();
            content = content[0].lower().translate(punctuation).split(' ')

            content = list(filter(lambda w: w != '', map(lambda s: s.strip(), content)))

            term_positions = find_positions(content)

            for key in term_positions:
                index.add_term(stemmer.stem(key), documentID, term_positions[key])
    except FileNotFoundError as e:
        i = 0
        print(e)