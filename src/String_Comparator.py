import re
from nltk.util import ngrams
from nltk.corpus import wordnet
import nltk
from thefuzz import fuzz

from src import Code_Tokenizer

sno = nltk.stem.SnowballStemmer('english')
import spacy

nlp = spacy.load('en_core_web_md')


def jaccard_similarity(str1, str2, n):
    str1_bigrams = list(ngrams(str1, n))
    str2_bigrams = list(ngrams(str2, n))

    intersection = len(list(set(str1_bigrams).intersection(set(str2_bigrams))))
    union = (len(set(str1_bigrams)) + len(set(str2_bigrams))) - intersection

    return float(intersection) / union


def word2vec(word):
    from collections import Counter
    from math import sqrt

    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c * c for c in cw.values()))

    # return a tuple
    return cw, sw, lw


def cosdis(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # print(v1, ",", v2)
    # by definition of cosine distance we have
    return sum(v1[0][ch] * v2[0][ch] for ch in common) / v1[2] / v2[2]


def get_text_to_number_equivalent(word):
    return '0' if word == 'zero' else '1' if word == 'one' else '2' if word == 'two' else '3' if word == 'three' else '4' if word == 'four' else '5' if word == 'five' else '6' if word == 'six' else '7' if word == 'seven' else '8' if word == 'eight' else '9' if word == 'nine' else word


def get_number_to_text_equivalent(word):
    return 'zero' if word == '0' else 'one' if word == '1' else 'two' if word == '2' else 'three' if word == '3' else 'four' if word == '4' else 'five' if word == '5' else 'six' if word == '6' else 'seven' if word == '7' else 'eight' if word == '8' else 'nine' if word == '9' else word


def normalize_text_to_number(target):
    for word in target:
        if get_text_to_number_equivalent(word) not in target:
            target.append(get_text_to_number_equivalent(word))
        if get_number_to_text_equivalent(word) not in target:
            target.append(get_number_to_text_equivalent(word))


def check_similarity_ddc_operand(ddc, operand, refine_method, threshold, special_characters_flag, camel_case_flag):
    # extract the different words from the operand
    operand = re.sub("[^a-zA-Z0-9]+", " ", operand.lower()).split()
    # normalize the number to text from operands
    normalize_text_to_number(operand)

    # filter the ddcs for java keywords
    ddc_filtered_keywords = Code_Tokenizer.get_tokenized_words(ddc[6], special_characters_flag, camel_case_flag)
    # normalize the number to text from tokens
    normalize_text_to_number(ddc_filtered_keywords)

    flag = False
    # check against "equal" between operand and code
    if refine_method == 0:
        for elem in ddc_filtered_keywords:
            for word in operand:
                if elem == word:
                    flag = True

    # check against "contains" between operand and code
    elif refine_method == 1:
        for elem in ddc_filtered_keywords:
            for word in operand:
                if (elem in word) or (word in elem):
                    flag = True

    # check against "contains" between operand and code + Class
    elif refine_method == 2:
        # add the Class name to the DDC tokens
        ddc_filtered_keywords.append(ddc[2].lower().split(".")[0])
        for elem in ddc_filtered_keywords:
            for word in operand:
                if (elem in word) or (word in elem):
                    flag = True

    # check against "contains" between operands + synonyms and code + Class
    elif refine_method == 3:
        # add the Class name to the DDC tokens
        ddc_filtered_keywords.append(ddc[2].lower().split(".")[0])

        # add synonyms to the operands
        synonyms = operand.copy()
        for word in operand:
            for syn in wordnet.synsets(word):
                for l in syn.lemmas():
                    synonyms.append(l.name())

        for elem in ddc_filtered_keywords:
            for word in synonyms:
                if (elem in word) or (word in elem):
                    flag = True

    # check against "equal" between operand lemma and code lemma
    elif refine_method == 4:
        for elem in ddc_filtered_keywords:
            for word in operand:
                if (sno.stem(elem) == sno.stem(word)) or (sno.stem(word) == sno.stem(elem)):
                    flag = True

    # check against "contains" between operand lemma and code + Class lemma
    elif refine_method == 5:
        # add the Class name to the DDC tokens
        ddc_filtered_keywords.append(ddc[2].lower().split(".")[0])

        for elem in ddc_filtered_keywords:
            for word in operand:
                if (sno.stem(elem) in sno.stem(word)) or (sno.stem(word) in sno.stem(elem)):
                    flag = True

    # check against nlp word similarity between operand and code
    elif refine_method == 6:
        for elem in ddc_filtered_keywords:
            for word in operand:
                if nlp(elem).similarity(nlp(word)) > threshold:
                    flag = True

    # check against jacquard similarity between operand and code
    elif refine_method == 7:
        for elem in ddc_filtered_keywords:
            for word in operand:
                if jaccard_similarity(elem, word, 1) > threshold:
                    flag = True

    # check against cosine distance similarity between operand and code
    elif refine_method == 8:
        for elem in ddc_filtered_keywords:
            for word in operand:
                if cosdis(word2vec(elem), word2vec(word)) > threshold:
                    flag = True

    # check against levenstein distance similarity between operand and code
    elif refine_method == 9:
        for elem in ddc_filtered_keywords:
            for word in operand:
                if fuzz.ratio(word, elem) > threshold * 100:
                    flag = True

    # check against levenstein distance similarity with a partial match between operand and code
    elif refine_method == 10:
        for elem in ddc_filtered_keywords:
            for word in operand:
                if fuzz.partial_ratio(word, elem) > 65:
                    flag = True

    # check against "contains" between operands + synonyms and code
    elif refine_method == 11:
        # add synonyms to the operands
        synonyms = operand.copy()
        for word in operand:
            for syn in wordnet.synsets(word):
                for l in syn.lemmas():
                    synonyms.append(l.name())

        for elem in ddc_filtered_keywords:
            for word in synonyms:
                if (elem in word) or (word in elem):
                    flag = True

    else:
        print('ERROR. Command not found.')
        exit - 1

    return flag


def get_tokens_ddc_operand(ddc, operand, tokens, refine_method, threshold, special_characters_flag, camel_case_flag):
    # extract the different words from the operand
    operand = re.sub("[^a-zA-Z0-9]+", " ", operand.lower()).split()
    # normalize the number to text from operands
    normalize_text_to_number(operand)

    # filter the ddcs for java keywords
    ddc_filtered_keywords = Code_Tokenizer.get_tokenized_words(ddc[6], special_characters_flag, camel_case_flag)
    # normalize the number to text from tokens
    normalize_text_to_number(ddc_filtered_keywords)

    # check against "equal" between operand and code
    if refine_method == 0:
        for elem in ddc_filtered_keywords:
            for word in operand:
                if (elem == word) and (elem not in tokens) and (len(elem) > len(word)/2):
                    tokens.append(elem)

    # check against "contains" between operand and code
    elif refine_method == 1:
        for elem in ddc_filtered_keywords:
            for word in operand:
                if ((elem in word) or (word in elem)) and (elem not in tokens) and (len(elem) > len(word)/2):
                    tokens.append(elem)

    return tokens


def check_similarity_esc_ddc(esc, ddc_token, special_characters_flag, camel_case_flag):
    # filter the escs for java keywords
    esc_filtered_keywords = Code_Tokenizer.get_tokenized_words(esc[6], special_characters_flag, camel_case_flag)
    # normalize the number to text from operands and tokens
    normalize_text_to_number(esc_filtered_keywords)

    flag = False
    # check against "equal" between ddc_token and esc_tokens
    for elem in esc_filtered_keywords:
        if elem == ddc_token:
            flag = True

    return flag
