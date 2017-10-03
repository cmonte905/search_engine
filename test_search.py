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

def test_index_txt_file():
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

    correct_map = {}
    correct_map['today'] = [posting(1, [0]), posting(2, [0]), posting(3, [0])]
    correct_map['i'] = [posting(1, [1, 6, 11]), posting(2, [1]), posting(3, [1]), posting(4, [0])]
    correct_map['fell'] = [posting(1, [2])]
    correct_map['in'] = [posting(1, [3])]
    correct_map['a'] = [posting(1, [4])]
    correct_map['well'] = [posting(1, [5])]
    correct_map['have'] = [posting(1, [7]), posting(4, [1])]
    correct_map['no'] = [posting(1, [8]), posting(5, [8])]
    correct_map['mouth'] = [posting(1, [9])]
    correct_map['but'] = [posting(1, [10])]
    correct_map['want'] = [posting(1, [12])]
    correct_map['to'] = [posting(1, [13])]
    correct_map['scream'] = [posting(1, [14])]
    correct_map['top'] = [posting(2, [2])]
    correct_map['deck'] = [posting(2, [3])]
    correct_map['lethal'] = [posting(2, [4])]
    correct_map['yogg'] = [posting(2, [5])]
    correct_map['saron'] = [posting(2, [5])]
    correct_map['yoggsaron'] = [posting(2, [5])]
    correct_map['fuck'] = [posting(2, [6])]
    correct_map['me'] = [posting(2, [7]), posting(4, [8])]
    correct_map['over'] = [posting(2, [8])]
    correct_map['super'] = [posting(2, [9])]
    correct_map['hard'] = [posting(2, [10])]
    correct_map['learn'] = [posting(3, [2])]
    correct_map['the'] = [posting(3, [3]), posting(5, [2])]
    correct_map['mean'] = [posting(3, [4])]
    correct_map['of'] = [posting(3, [5])]
    correct_map['pain'] = [posting(3, [6])]
    correct_map['it'] = [posting(3, [7]), posting(4, [9]), posting(5, [12])]
    correct_map['was'] = [posting(3, [8]), posting(4, [10])]
    correct_map['all'] = [posting(3, [9])]
    correct_map['caus'] = [posting(3, [10])]
    correct_map['by'] = [posting(3, [11])]
    correct_map['nealdt'] = [posting(3, [12])]
    correct_map['ascend'] = [posting(4, [2])]
    correct_map['into'] = [posting(4, [3])]
    correct_map['enlighten'] = [posting(4, [4])]
    correct_map['my'] = [posting(4, [5])]
    correct_map['waifu'] = [posting(4, [6])]
    correct_map['told'] = [posting(4, [7])]
    correct_map['actual'] = [posting(4, [11])]
    correct_map['okay'] = [posting(4, [12])]
    correct_map['jesus'] = [posting(5, [0])]
    correct_map['take'] = [posting(5, [1])]
    correct_map['wheel'] = [posting(5, [3])]
    correct_map['or'] = [posting(5, [4])]
    correct_map['els'] = [posting(5, [5])]
    correct_map['asian'] = [posting(5, [6])]
    correct_map['driver'] = [posting(5, [7])]
    correct_map['survivor'] = [posting(5, [9])]
    correct_map['dont'] = [posting(5, [10])]
    correct_map['let'] = [posting(5, [11])]
    correct_map['happen'] = [posting(5, [13])]

    for keys in txt_index.get_index():
        assert keys in correct_map

def test_query():
    correct_map = {}
    correct_map['today'] = [posting(1, [0]), posting(2, [0]), posting(3, [0])]
    correct_map['i'] = [posting(1, [1, 6, 11]), posting(2, [1]), posting(3, [1]), posting(4, [0])]
    correct_map['fell'] = [posting(1, [2])]
    correct_map['in'] = [posting(1, [3])]
    correct_map['a'] = [posting(1, [4])]
    correct_map['well'] = [posting(1, [5])]
    correct_map['have'] = [posting(1, [7]), posting(4, [1])]
    correct_map['no'] = [posting(1, [8]), posting(5, [8])]
    correct_map['mouth'] = [posting(1, [9])]
    correct_map['but'] = [posting(1, [10])]
    correct_map['want'] = [posting(1, [12])]
    correct_map['to'] = [posting(1, [13])]
    correct_map['scream'] = [posting(1, [14])]
    correct_map['top'] = [posting(2, [2])]
    correct_map['deck'] = [posting(2, [3])]
    correct_map['lethal'] = [posting(2, [4])]
    correct_map['yogg'] = [posting(2, [5])]
    correct_map['saron'] = [posting(2, [5])]
    correct_map['yoggsaron'] = [posting(2, [5])]
    correct_map['fuck'] = [posting(2, [6])]
    correct_map['me'] = [posting(2, [7]), posting(4, [8])]
    correct_map['over'] = [posting(2, [8])]
    correct_map['super'] = [posting(2, [9])]
    correct_map['hard'] = [posting(2, [10])]
    correct_map['learn'] = [posting(3, [2])]
    correct_map['the'] = [posting(3, [3]), posting(5, [2])]
    correct_map['mean'] = [posting(3, [4])]
    correct_map['of'] = [posting(3, [5])]
    correct_map['pain'] = [posting(3, [6])]
    correct_map['it'] = [posting(3, [7]), posting(4, [9]), posting(5, [12])]
    correct_map['was'] = [posting(3, [8]), posting(4, [10])]
    correct_map['all'] = [posting(3, [9])]
    correct_map['caus'] = [posting(3, [10])]
    correct_map['by'] = [posting(3, [11])]
    correct_map['nealdt'] = [posting(3, [12])]
    correct_map['ascend'] = [posting(4, [2])]
    correct_map['into'] = [posting(4, [3])]
    correct_map['enlighten'] = [posting(4, [4])]
    correct_map['my'] = [posting(4, [5])]
    correct_map['waifu'] = [posting(4, [6])]
    correct_map['told'] = [posting(4, [7])]
    correct_map['actual'] = [posting(4, [11])]
    correct_map['okay'] = [posting(4, [12])]
    correct_map['jesus'] = [posting(5, [0])]
    correct_map['take'] = [posting(5, [1])]
    correct_map['wheel'] = [posting(5, [3])]
    correct_map['or'] = [posting(5, [4])]
    correct_map['els'] = [posting(5, [5])]
    correct_map['asian'] = [posting(5, [6])]
    correct_map['driver'] = [posting(5, [7])]
    correct_map['survivor'] = [posting(5, [9])]
    correct_map['dont'] = [posting(5, [10])]
    correct_map['let'] = [posting(5, [11])]
    correct_map['happen'] = [posting(5, [13])]




    q = Query(correct_map)

    s1 = '\"tAke the wheel\"'

    s2 = 'Today'

    s1_list = q.query_parser(s1)

    s2_list = q.query_parser(s2)



    assert s1_list == [5] 
    assert s2_list == [1, 2, 3]



