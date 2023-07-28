import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''
    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    return math.sqrt(sum_of_squares)

def cosine_similarity(vec1, vec2):
    '''return the cosine similarity of the two vector dicts,
    by taking dot product of common items and div by mag'''
    dot, mag1, mag2 = 0, 0, 0
    for i in vec1:
        if i in vec2:
            dot += vec1[i] *vec2[i]
        mag1 += vec1[i]**2
    for i in vec2:
        mag2 += vec2[i]**2

    return dot/(math.sqrt(mag1*mag2))


def build_semantic_descriptors(sentences):
    '''return a dictionary of all words in sentences, with the # of
    occurrences of each word'''

    d = {}

    for sentence in sentences:
        word_list = list(set([j for j in sentence]))
        for key in word_list:
            if key not in d:
                d[key] = {}
            for w in sentence:
                if key != w:
                    if w not in d[key]:
                        d[key][w] = 1
                    else:
                        d[key][w] += 1

    return d



def build_semantic_descriptors_from_files(filenames):
    '''take filenames (list), and then open each one and return a dict of
    filenames from semantic_descriptors(sentences). treat filenames as 1 text'''

    masterlist = []

    for file in filenames:
        f = open(file,"r",encoding="utf-8")
        file = f.read()
        file_org = file_punc_cleaner(file)
        for j in file_org:
            masterlist.append(j)
    return build_semantic_descriptors(masterlist)

def file_punc_cleaner(file):
    ch_start = 0
    lst = []

    '''return a list in the format of [[word,word,word],[sentence],...]'''

    for ch in range(len(file)):
        if file[ch] in ['?','.','!']:
            lst += [[file[ch_start:ch]]]
            ch_start = ch+2

    for s in range(len(lst)):
        for i in range(len(lst[s])):
            for ch in lst[s][i]:
                if ch in [",", "-", "--", ":", ";","\"","(",")"]:
                    lst[s][i] = (lst[s][i]).replace(ch," ")
            lst[s] = lst[s][i].lower().split()

    return lst


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    '''calculate similarity btwn word's semantic descriptors
    and each choice from choices's semantic descirptors, return most similar to word'''

    similarities = []

    if word not in semantic_descriptors:
        return -1
    for choice in choices:
        if choice not in semantic_descriptors:
            similarities.append(-1)
        elif semantic_descriptors[choice] == {}:
            similarities.append(-1)
        else:
            similarities.append(similarity_fn(semantic_descriptors[choice],semantic_descriptors[word]))

    return choices[similarities.index(max(similarities))]

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    '''return % of q answered correctly by semantics reader'''
    score = 0
    tests = open(filename, "r",encoding="utf-8").read().lower().split('\n')
    clean_tests = [i.split() for i in tests]
    for test in clean_tests:
        if most_similar_word(test[0],test[2:],semantic_descriptors,similarity_fn) == test[1]:
            score += 1

    return score/len(tests)  * 100
