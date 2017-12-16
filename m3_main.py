from os import listdir
from math import log, sqrt, pow
import string
import re

# Custom Classes
from positional_inverted_index import positional_inverted_index

# Porter 2 Stemmer
from porter2stemmer import Porter2Stemmer


# The Index
# { index[term] : [<ID, [p1, p2,... pk]>, <ID, [p1, p2,... pk]>, ...] }
all_docs_index = positional_inverted_index()
doc_wdt = {}
doc_total_tf = {}

ALL_DIR = '/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/ALL/'
JAY_DIR = '/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/JAY/'
HAMILTON_DIR = '/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/HAMILTON/'
MADISON_DIR = '/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/MADISON/'
DISPUTED_DIR = '/Users/Cemo/Documents/cecs429/search_engine/federalist-papers/DISPUTED/'

# Rocchio vectors/centroids
r_ham_vector = {}
r_mad_vector = {}
r_jay_vector = {}

# p(t | c)
ptc_map = {}  # {term : {class: ptc }}

# Bayesian ptc vars
b_ham_freq_vector = {}
b_mad_freq_vector = {}
b_jay_freq_vector = {}

author_term_map = {}

# List of vocab tokens for terms in the corpus
# Dictionary <String : List[String]>


def index_file(directory, file_name, documentID, index):
    stemmer = Porter2Stemmer()
    # Dealing with punctuation
    p = dict.fromkeys(string.punctuation)
    p.pop('-')  # we need to deal with hyphens
    weight_map = {}

    try:
        with open(directory + file_name) as txt_file:
            # Trying to normalize the vocab, getting rid of non alphanumeric,
            body = txt_file.read().replace('\n', '').lower()
            body = re.sub(r'[^A-Za-z0-9#]+', ' ', body)
            body = body.split(' ')  # Gets rid of any \n that appear in the text

            body = list(filter(lambda t: t != '' and t != '-', body))  # remove single spaces and single hyphens

            position = 0
            for term in body:
                # take care of hyphenated words
                if '-' in term:
                    unhyphenated_word = term.replace('-', '')
                    index.add_term(stemmer.stem(unhyphenated_word), documentID, position)
                    hyphened_tokens = term.split('-')
                    for t in hyphened_tokens:
                        all_docs_index.add_term(stemmer.stem(t), documentID, position)
                else:
                    index.add_term(stemmer.stem(term), documentID, position)
                position += 1
                if term not in weight_map:
                    weight_map[term] = 1
                else:
                    weight_map[term] = weight_map[term] + 1

    except FileNotFoundError as e:
        print(e)

    doc_total_tf[file_name] = weight_map  # given a document, it will return a map of that docs tf

    score_map = {}
    wdt = 0
    # Gets the Wdt's of the terms in the file
    for tf in weight_map:
        score = pow(1 + log(weight_map[tf]), 2)
        score_map[tf] = score
        wdt += score**2
    Ld = sqrt(wdt)
    length = 0
    for tf in score_map:
        score_map[tf] = score_map[tf]/Ld
        length += score_map[tf]**2

    doc_wdt[file_name] = score_map
    # Things to turn in for Neal, it's just the easiest place to put this
    if file_name == 'paper_52.txt':
        print('First 30 components of document 52')
        get_first_thirty(score_map, True)

# ----------------------------------------------------------------------------------------------------------------
# Rocchio stuff - Got too lazy to put into separate classes like a good software engineer


def train_rocchio(class_list, docs, name):
    """
    Trains the class given list of documents to look at
    :param class_list: List of docs, these files are the ones that get associated with the class
    :param docs: Map of <doc : <term : score>>
    :param name: The class that is getting trained, associated with a global map of that classes centroid
    :return:
    """
    if name == 'hamilton':
        vec = r_ham_vector
    elif name == 'madison':
        vec = r_mad_vector
    else:
        vec = r_jay_vector

    for i in docs:
        if i in class_list:
            inner_map = docs[i]
            for j in inner_map:
                if j not in vec:
                    vec[j] = inner_map[j]
                else:
                    vec[j] = vec[j] + inner_map[j]

    for i in vec:
        vec[i] = vec[i]/len(class_list)
    print('\nFirst thirty values of centroid {}'. format(name))
    get_first_thirty(vec, True)


def apply_rocchio(disputed_file):
    """

    :param disputed_file:
    :return:
    """
    scores = [0.0, 0.0, 0.0]  # Hamilton, Madison, and Jay respectively
    disputed_index = doc_wdt[disputed_file]

    sum_vec = 0.0
    for i in disputed_index:
        if i in r_ham_vector:
            sum_vec += pow(r_ham_vector[i] - disputed_index[i], 2)
        else:
            sum_vec += pow(disputed_index[i], 2)
    scores[0] = sqrt(sum_vec)
    sum_vec = 0.0
    for i in disputed_index:
        if i in r_mad_vector:
            sum_vec += pow(r_mad_vector[i] - disputed_index[i], 2)
        else:
            sum_vec += pow(disputed_index[i], 2)
    scores[1] = sqrt(sum_vec)
    sum_vec = 0.0
    for i in disputed_index:
        if i in r_jay_vector:
            sum_vec += pow(r_jay_vector[i] - disputed_index[i], 2)
        else:
            sum_vec += pow(disputed_index[i], 2)
    scores[2] = sqrt(sum_vec)

    if disputed_file == 'paper_52.txt':
        print('\nEuclidians distance between the normalized vector for the document and each of the 3 class centroids')
        print('Hamilton {0} | Madison {1} | Jay {2}\n'.format(scores[0], scores[1], scores[2]))

    if scores[0] < scores[1] and scores[0] < scores[2]:
        print('{0} was written by Hamilton'.format(disputed_file))
    elif scores[1] < scores[0] and scores[1] < scores[2]:
        print('{0} was written by Madison'.format(disputed_file))
    else:
        print('{0} was written by Jay'.format(disputed_file))


def get_first_thirty(index, values=False):
    """
    Gets the first thirty words in the vocabulary for turn in for Rocchio
    :param index: A map to use to print out
    :param values: Option to print values if needed
    """
    counter = 1
    for i, j in sorted(index.items()):
        if counter <= 30 and values:
            print(counter, i, ':', j)
        elif counter <= 30:
            print(counter, i)
        counter += 1
    print('\n')

# End of Rocchio stuff

# ----------------------------------------------------------------------------------------------------------------
# Bayesian stuff


def bayesian_apply(disputed_file, class_lists):
    scores = []
    disputed_term_map = doc_total_tf[disputed_file]
    for c in range(3):  # Classes are Jay, Hamilton and Madison
        if c == 0:
            class_name = 'jay'
        elif c == 1:
            class_name = 'hamilton'
        else:
            class_name = 'madison'
        prob_of_t_in_c = 0
        prob_of_c = log(len(class_lists[c]) / len(get_list_files(ALL_DIR)), 2)
        for d in disputed_term_map:
            if d in ptc_map:
                prob_of_t_in_c += ptc_map[d][class_name]

        if prob_of_t_in_c == 0:
            score = prob_of_c
        else:
            score = prob_of_c + log(prob_of_t_in_c, 2)

        scores.append(score)
    if disputed_file == 'paper_49.txt':
        print('Jay score : {0} | Hamilton score : {1} | Madison score {2}'.format(scores[0], scores[1], scores[2]))

    if scores[1] > scores[0] and scores[1] > scores[2]:
        print('Given Bayesian : {0} is written by Hamilton'.format(disputed_file))
    elif scores[2] > scores[0] and scores[2] > scores[1]:
        print('Given Bayesian : {0} is written by Madison'.format(disputed_file))
    elif scores[0] > scores[1] and scores[0] > scores[2]:
        print('Given Bayesian : {0} is written by Jay'.format(disputed_file))


def calculate_itc(term, class_files):
    N = len(get_list_files(ALL_DIR))  # corpus size
    N11 = 0  # Number of docs that is part of the class and contains the term
    for docs in class_files:  # gets
        # print('class files', docs)
        if docs in doc_total_tf:
            if term in doc_total_tf[docs]:
                N11 += 1
    N1x = N11  # Number of documents that contain the the word
    for docs in doc_total_tf:
        if docs not in class_files:
            N1x += 1
    Nx1 = len(class_files)
    Nx0 = N - Nx1  # Number of documents not in the class
    N0x = N - N1x  # Number of documents that not contain the term
    N01 = Nx1 - N11
    N10 = N1x - N11
    N00 = Nx0 - N10

    n1 = (N11 / N) * itc_helper((N * N11), (N1x * Nx1))
    n2 = (N10 / N) * itc_helper((N * N10), (N1x * Nx0))
    n3 = (N01 / N) * itc_helper((N * N01), (N0x * Nx1))
    n4 = (N00 / N) * itc_helper((N * N00), (N0x * Nx0))

    return n1 + n2 + n3 + n4


def itc_helper(a, b):
    if a * b == 0:
        return 0
    return log((a/b), 2)


def get_max_itc(term, classes_dirs):
    counter = 0
    class_name = 0
    max_itc = 0
    for i in classes_dirs:
        itc_value = calculate_itc(term, i)
        if max_itc < itc_value:
            max_itc = itc_value
            class_name = counter
        counter += 1

    author_term_map[term] = class_name
    return max_itc


def bayesian_init(disc_len, vocab, classes_dirs, ten=False):
    """
    Gets back the top k terms
    :param disc_len: Number of discrete terms wanted
    :param vocab: All terms in the corpus's vocab
    :param classes_dirs: List of directory lists
    :param ten:  If its true, print out the first ten I(T|C) scores and the docs
    :return:
    """
    discrimiate_list = []
    itc_map = {}
    itc_value_list = []

    for term in vocab:
        itc_value = get_max_itc(term, classes_dirs)

        if itc_value in itc_map:
            itc_map[itc_value].append(term)
        else:
            itc_map[itc_value] = [term]

        if itc_value not in itc_value_list:
            itc_value_list.append(itc_value)

    for val in sorted(itc_value_list, reverse=True):
        for term in itc_map[val]:
            if ten:
                print('Term: {0} | I(T,C): {1}'.format(term, val))
            discrimiate_list.append(term)
            if len(discrimiate_list) == disc_len:
                return discrimiate_list


def calc_ptc(class_vec, term, term_size, sum_ftc):
    if term not in class_vec:
        numerator = 1  # Numerator
    else:
        numerator = 1 + class_vec[term]  # Numerator
    denomator = sum_ftc + term_size   # Denomator
    return numerator/denomator


def generate_feature_vector(t_list, class_doc_list, class_name, vec):
    """
    Pass in class doc list, it will get the term frequencies of those docs
    :param t_list:
    :param class_doc_list: Class document list, documents that pertain to a class
    :param class_name:
    :param vec : Class frequency vector
    :return:
    """
    sum_ftc = 0  # Σ of all terms frequencies in a class
    sum_map = {}  # <class, sum of ftc> Inner map of ptc map, key is word
    for i in class_doc_list:  # Goes through every document that belongs to a class
        if i in doc_total_tf:  # if key is in class's document list
            for term in doc_total_tf[i]:  # Document's term frequencies
                if term not in vec:
                    vec[term] = doc_total_tf[i][term]
                else:
                    vec[term] = vec[term] + doc_total_tf[i][term]
                sum_ftc += doc_total_tf[i][term]  # Value of that documents term frequencies
    sum_map[class_name] = sum_ftc

    for i in t_list:
        ptc = calc_ptc(vec, i, len(t_list), sum_ftc)
        if i not in ptc_map:
            ptc_map[i] = {class_name: ptc}
        else:
            ptc_map[i].update({class_name: ptc})

# End of Bayesian
# ----------------------------------------------------------------------------------------------------------------


def get_list_files(directory):
    """
    Gets a list of files in a given directory sorted by their document number since python does not do this sort of
    thing natively, probably something to do with the OS.
    :param directory:
    :return: List of docs in sorted order
    """
    file_names = []  # Names of files
    sorted_files = sorted(listdir(directory), key=lambda x: (int(re.sub('\D', '', x)), x))
    for file in sorted_files:
        if file.endswith('.txt'):
            file_names.append(str(file))
    return file_names


def init(directory, index):
    # file_names = []
    file_names = get_list_files(directory)

    # Index each file and mark its Document ID
    for file in file_names:
        index_file(directory, file, int(re.findall(r'\d+', file)[0]), index)


def main():
    # Federalist papers n shit, all of them
    jay_files = get_list_files(JAY_DIR)
    hamilton_files = get_list_files(HAMILTON_DIR)
    madison_files = get_list_files(MADISON_DIR)
    disputed_files = get_list_files(DISPUTED_DIR)

    init(ALL_DIR, all_docs_index)

    # -----------------------------------------------------------------------------------------------------------------
    # Rocchio Classification

    print('First thirty terms in the index')
    get_first_thirty(all_docs_index.get_index())

    train_rocchio(hamilton_files, doc_wdt, 'hamilton')
    train_rocchio(madison_files, doc_wdt, 'madison')
    train_rocchio(jay_files, doc_wdt, 'jay')

    for i in disputed_files:
        apply_rocchio(i)

    # -----------------------------------------------------------------------------------------------------------------
    # Bayesian Classification
    term_list = sorted(list(all_docs_index.get_index()))  # List of all terms in the corpus vocabulary
    all_class_dirs = [jay_files, hamilton_files, madison_files]

    print('\nUsing 10 top terms')
    discrimate_terms_list = bayesian_init(10, term_list, all_class_dirs, True)
    generate_feature_vector(discrimate_terms_list, jay_files, 'jay', b_jay_freq_vector)
    generate_feature_vector(discrimate_terms_list, hamilton_files, 'hamilton', b_ham_freq_vector)
    generate_feature_vector(discrimate_terms_list, madison_files, 'madison', b_mad_freq_vector)

    for d in disputed_files:
        bayesian_apply(d, all_class_dirs)

    print('\nUsing 50 top terms')
    discrimate_terms_list = bayesian_init(50, term_list, all_class_dirs)
    generate_feature_vector(discrimate_terms_list, jay_files, 'jay', b_jay_freq_vector)
    generate_feature_vector(discrimate_terms_list, hamilton_files, 'hamilton', b_ham_freq_vector)
    generate_feature_vector(discrimate_terms_list, madison_files, 'madison', b_mad_freq_vector)

    for d in disputed_files:
        bayesian_apply(d, all_class_dirs)

    # -----------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
