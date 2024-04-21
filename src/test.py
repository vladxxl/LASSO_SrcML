import re
import time

from src import Code_Tokenizer

xml_file = '/Users/vladb/PycharmProjects/srcML_Lasso/input/data/apache-ant-1.10.6/sources/src/main/org/apache/tools/ant/taskdefs/optional/PropertyFile.srcml.xml'


def clean_xml_namespaces(root):
    for elem in root.iter():
        elem.tag = re.sub(r"\{(.*?)\}", "", elem.tag)


if __name__ == '__main__':
    # tree = ET.parse(xml_file)
    # root = tree.getroot()
    # clean_xml_namespaces(root)
    #
    # print(len([elem.text for elem in root.iterfind('.//name')]))
    #
    # tree = ET.parse(xml_file)
    # clean_xml_namespaces(tree)

    # print(len([elem.text for elem in tree.iterfind('.//name')]))
    # print([elem.text for elem in tree.findall(".//name[.!='name']")])
    # print([''.join(elem.itertext()) for elem in tree.findall(".//decl")])
    # print([ET.tostring(elem) for elem in tree.findall(".//decl")])

    # with open('src/DDP.csv') as fp:
    #     reader = csv.reader(fp, delimiter=",", quotechar='"')
    #     data_read = [row for row in reader]
    # print(data_read)

    # folder = 'input/data'
    # sub_folders = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]
    # for system in sub_folders:
    #
    #     for root, dirs, files in os.walk(folder + '/' + system):
    #         for file in files:
    #             if file.endswith(".java"):

    # import subprocess
    # path = '/Users/vladb/PycharmProjects/srcML_Lasso/input/data/apache-ant-1.10.6/sources/src/main/org/apache/tools/ant/taskdefs/optional/PropertyFile.java'
    # # xpath_query = "//src:decl[not(self::src:decl/src:init/src:expr/src:name)] | //src:decl[src:init/src:expr/src:name/src:name]"
    # xpath_query = '//src:if/src:condition[descendant::src:literal[@type="string"]]'
    # test = subprocess.Popen(["srcml", "--position", "--xpath", xpath_query, path], stdout=subprocess.PIPE)
    # output = test.communicate()[0]
    #
    # # print(output)
    #
    # tree = ET.fromstring(output)
    # clean_xml_namespaces(tree)
    #
    # print(len(tree.findall('.//unit')))
    # for elem in tree.findall('.//unit/*'):
    #     print(''.join(elem.itertext()))
    #     # print(elem.tag, elem.text)

    # mylist = [['a',1,2],['a',2,3],['b',1,4]]
    # # unique values
    # values = set(map(lambda x: x[0], mylist))
    # newlist = [[y for y in mylist if y[0] == x] for x in values]
    # for el in newlist:
    #     print('Value: ', el[0][0], ' size:',  len(el))

    # ddc = [ 'apache-httpcomponents-4.5.9', 'input/data/apache-httpcomponents-4.5.9/sources/httpcomponents-core-4.4.11/httpcore/src/main/java/org/apache/http/impl', 'BHttpConnectionBase.java', '236:9', '236:82', 'INIT', 'final Header contentTypeHeader = message.getFirstHeader(HTTP.CONTENT_TYPE)']
    # operand = "`authorlastseparatorintext`"
    # print(DDC_Refinement.check_simmilarity(ddc,operand,1))

    # word = 'String andString = getStringCitProperty(AUTHOR_LAST_SEPARATOR_IN_TEXT)'.lower()
    # Java_Code_Tokenizer.get_filtered_words(word)

    # from nltk.corpus import wordnet
    #
    # synonyms = []
    #
    # for syn in wordnet.synsets("0"):
    #     for l in syn.lemmas():
    #         synonyms.append(l.name())
    #
    # print(set(synonyms))

    # import spacy
    #
    # nlp = spacy.load('en_core_web_md')
    #
    # book1_topics = ['Christ']
    # book2_topics = ['dog']
    #
    # doc1 = nlp(' '.join(book1_topics))
    # doc2 = nlp(' '.join(book2_topics))
    #
    # print(doc1.similarity(doc2))
    #
    # print(doc2.similarity(doc1))

    # from nltk.util import ngrams
    #
    #
    # def jaccard_similarity(str1, str2, n):
    #     str1_bigrams = list(ngrams(str1, n))
    #     str2_bigrams = list(ngrams(str2, n))
    #
    #     intersection = len(list(set(str1_bigrams).intersection(set(str2_bigrams))))
    #     union = (len(set(str1_bigrams)) + len(set(str2_bigrams))) - intersection
    #
    #     return float(intersection) / union
    #
    # print(jaccard_similarity('chrstian', 'christianity', 1))
    # print(jaccard_similarity('Chrstian', 'christianity', 2))
    # print(jaccard_similarity('chrstian', 'christianity', 3))
    # print(jaccard_similarity('chrstian', 'christianity', 4))
    # print(jaccard_similarity('chrstian', 'christianity', 5))
    #
    # print()
    #
    # print(jaccard_similarity('god', 'godly', 1))
    # print(jaccard_similarity('god', 'godly', 2))
    # print(jaccard_similarity('god', 'godly', 3))
    # print(jaccard_similarity('god', 'godly', 4))
    # print(jaccard_similarity('god', 'godly', 5))

    # def word2vec(word):
    #     from collections import Counter
    #     from math import sqrt
    #
    #     # count the characters in word
    #     cw = Counter(word)
    #     # precomputes a set of the different characters
    #     sw = set(cw)
    #     # precomputes the "length" of the word vector
    #     lw = sqrt(sum(c * c for c in cw.values()))
    #
    #     # return a tuple
    #     return cw, sw, lw
    #
    #
    # def cosdis(v1, v2):
    #     # which characters are common to the two words?
    #     common = v1[1].intersection(v2[1])
    #     # by definition of cosine distance we have
    #     return sum(v1[0][ch] * v2[0][ch] for ch in common) / v1[2] / v2[2]
    #
    #
    # a = 'christian'
    # b = 'christianity'
    #
    # va = word2vec(a)
    # vb = word2vec(b)
    #
    # print(cosdis(va, vb))
    # print(cosdis(vb, va))

    # from thefuzz import fuzz
    #
    # print(fuzz.ratio("this is a test", "this is a test!"))
    # print(fuzz.partial_ratio("this is a test", "this is a test!"))

    # import sctokenizer
    #
    # tokens = sctokenizer.tokenize_str('final Header contentLengthHeader = message.getFirstHeader(HTTP.CONTENT_LEN);', lang='java')
    # for token in tokens:
    #     l = str(token).replace("(", '').replace(")", '').split(',')
    #     print(token.token_value)

    # import re
    # from enum import Enum
    #
    #
    # class TokenType(Enum):
    #     integer = 1
    #     float = 2
    #     bool = 3
    #     string = 4
    #
    #
    # # note: order is important! most generic patterns always go to the bottom
    # scanner = re.Scanner([
    #     (r"\d+\.\d*", lambda s, t: (TokenType.float, float(t))),
    #     (r"\d+", lambda s, t: (TokenType.integer, int(t))),
    #     (r"true|false+", lambda s, t: (TokenType.bool, t == "true")),
    #     (r"'[^']+'", lambda s, t: (TokenType.string, t[1:-1])),
    #     (r"\w+", lambda s, t: (TokenType.string, t)),
    #     (r".", lambda s, t: None),  # ignore unmatched parts
    # ])
    #
    # input = "final Header contentLengthHeader = message.getFirstHeader(HTTP.CONTENT_LEN);"
    #
    # start_time1 = time.time()
    #
    # # "unknown" contains unmatched text, check it for error handling
    # tokens, unknown = scanner.scan(input)
    #
    # # for t_type, t_val in tokens:
    # #     print(t_val)
    #
    # print("--- First in %s seconds ---" % (time.time() - start_time1))

    # import javalang
    #
    # start_time2 = time.time()
    #
    # tokens = list(javalang.tokenizer.tokenize('final Header contentLengthHeader = message.getFirstHeader(HTTP.CONTENT_LEN) + 3.45;'))
    # # # Modifier, Operator, Separator
    # for token in tokens:
    #     print(token.value)
    #
    # print("--- Second in %s seconds ---" % (time.time() - start_time2))




    # b = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<unit xmlns="http://www.srcML.org/srcML/src" revision="1.0.0">\n\n<unit revision="1.0.0" language="Java" item="1">entity</unit>\n\n<unit revision="1.0.0" language="Java" item="2">StringEntity</unit>\n\n<unit revision="1.0.0" language="Java" item="3">"<html><body><h1>File"</unit>\n\n<unit revision="1.0.0" language="Java" item="4">file</unit>\n\n<unit revision="1.0.0" language="Java" item="5">getPath</unit>\n\n<unit revision="1.0.0" language="Java" item="6">" not found</h1></body></html>"</unit>\n\n<unit revision="1.0.0" language="Java" item="7">ContentType</unit>\n\n<unit revision="1.0.0" language="Java" item="8">create</unit>\n\n<unit revision="1.0.0" language="Java" item="9">"text/html"</unit>\n\n<unit revision="1.0.0" language="Java" item="10">"UTF-8"</unit>\n\n</unit>\n'
    # from bs4 import BeautifulSoup
    # soup = BeautifulSoup(b, 'xml')
    #
    # names = soup.find_all('unit')
    # for name in names:
    #     print(name.text)
    #
    # import time

    # start_time = time.time()
    # code = 'final Header contentTypeHeader = message.getFirstHeader(HTTP.CONTENT_TYPE);'
    # print(Code_Tokenizer.get_tokenized_words(code, 0, False, 'Java'))
    # print("--- First in %s seconds ---" % (time.time() - start_time))
    #
    # start_time = time.time()
    # code = 'final Header contentTypeHeader = message.getFirstHeader(HTTP.CONTENT_TYPE);'
    # print(Code_Tokenizer.get_tokenized_words2(code, 0, False, 'Java'))
    # print("--- Second in %s seconds ---" % (time.time() - start_time))
    #
    # start_time = time.time()
    # code = 'final Header contentTypeHeader = message.getFirstHeader(HTTP.CONTENT_TYPE);'
    # print(Code_Tokenizer.get_tokenized_words3(code, 0, False, 'Java'))
    # print("--- Third in %s seconds ---" % (time.time() - start_time))
    #
    # start_time = time.time()
    # code = 'final Header contentTypeHeader = message.getFirstHeader(HTTP.CONTENT_TYPE);'
    # print(Code_Tokenizer.get_tokenized_words4(code, 0, False, 'Java'))
    # print("--- Fourth in %s seconds ---" % (time.time() - start_time))

    # import spacy
    #
    # nlp = spacy.load("en_core_web_md")  # make sure to use larger package!
    #
    #
    # start_time = time.time()
    # doc1 = nlp("I like salty fries and hamburgers.")
    # doc2 = nlp("Fast food tastes very good.")
    #
    # # Similarity of two documents
    # print(doc1, "<->", doc2, doc1.similarity(doc2))
    # print("--- First in %s seconds ---" % (time.time() - start_time))
    #
    # start_time = time.time()
    # print(nlp("I like salty fries and hamburgers.").similarity(nlp("Fast food tastes very good.")))
    #
    # print("--- First B in %s seconds ---" % (time.time() - start_time))

    # # Similarity of tokens and spans
    # french_fries = doc1[2:4]
    # burgers = doc1[5]
    # print(french_fries, "<->", burgers, french_fries.similarity(burgers))
    #
    # print(doc2, "<->", doc1, doc2.similarity(doc1))
    # print(french_fries, "<->", doc1, french_fries.similarity(doc1))

    # nlp = spacy.load("en_core_web_lg")  # make sure to use larger package!
    #
    # start_time = time.time()
    # doc1 = nlp("I like salty fries and hamburgers.")
    # doc2 = nlp("Fast food tastes very good.")
    #
    # # Similarity of two documents
    # print(doc1, "<->", doc2, doc1.similarity(doc2))
    # print("--- Second in %s seconds ---" % (time.time() - start_time))
    #
    # start_time = time.time()
    # print(nlp("I like salty fries and hamburgers.").similarity(nlp("Fast food tastes very good.")))
    #
    # print("--- Second B in %s seconds ---" % (time.time() - start_time))

    help_dict = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
        'zero': '0'
    }

    # initializing string
    test_str = "zero nothing zero one"
    test_str2 = "zero nine zero one"

    # start_time = time.time()
    # res = ''.join(help_dict[ele] for ele in test_str.split())
    # print(res)
    # print("--- First in %s seconds ---" % (time.time() - start_time))
    #
    #
    # from word2number import w2n
    #
    # start_time = time.time()
    # res = w2n.word_to_num(test_str)
    # print(str(res))
    # res = w2n.word_to_num(test_str2)
    # print(str(res))
    # print("--- Second in %s seconds ---" % (time.time() - start_time))
    #
    # import re
    #
    #
    # def convert_to_numbers(s):
    #     words_to_numbers = {
    #         'one': '1',
    #         'two': '2',
    #         'three': '3',
    #         'four': '4',
    #         'five': '5',
    #         'six': '6',
    #         'seven': '7',
    #         'eight': '8',
    #         'nine': '9',
    #         'zero': '0'
    #     }
    #
    #     pattern = re.compile(r'\b(' + '|'.join(words_to_numbers.keys()) + r')\b')
    #     return re.sub(pattern, lambda x: words_to_numbers[x.group()], s)
    #
    #
    # start_time = time.time()
    # print(convert_to_numbers(test_str))
    # print(convert_to_numbers(test_str2))
    # print("--- Third in %s seconds ---" % (time.time() - start_time))

    # start_time = time.time()
    # # Split the input string into words
    # words = test_str.split()
    #
    # # Map each word to its corresponding digit using the dictionary
    # digits = [help_dict[word] for word in words]
    #
    # # Join the resulting list of digits into a string
    # result = ''.join(digits)
    # print(result)
    #
    # # Split the input string into words
    # words = test_str2.split()
    #
    # # Map each word to its corresponding digit using the dictionary
    # digits = [help_dict[word] for word in words]
    #
    # # Join the resulting list of digits into a string
    # result = ''.join(digits)
    # print(result)
    # print("--- Fourth in %s seconds ---" % (time.time() - start_time))

    # start_time = time.time()
    # result = ''.join(['0' if word == 'zero' else '1' if word == 'one' else '2' if word == 'two' else '3' if word == 'three' else '4' if word == 'four' else '5' if word == 'five' else '6' if word == 'six' else '7' if word == 'seven' else '8' if word == 'eight' else '9' if word == 'nine' else word
    #                      for word in test_str.split()])
    #
    # print(result)
    # result = ''.join([
    #                      '0' if word == 'zero' else '1' if word == 'one' else '2' if word == 'two' else '3' if word == 'three' else '4' if word == 'four' else '5' if word == 'five' else '6' if word == 'six' else '7' if word == 'seven' else '8' if word == 'eight' else '9' if word == 'nine' else word
    #                      for word in test_str2])
    #
    # print(result)
    # print("--- fifth in %s seconds ---" % (time.time() - start_time))
    #
    # start_time = time.time()
    # number=92502
    # result =  ' '.join([
    #     'zero' if word == '0' else 'one' if word == '1' else 'two' if word == '2' else 'three' if word == '3' else 'four' if word == '4' else 'five' if word == '5' else 'six' if word == '6' else 'seven' if word == '7' else 'eight' if word == '8' else 'nine' if word == '9' else word
    #     for word in str(number)])
    # print(result)
    # print("--- sixth in %s seconds ---" % (time.time() - start_time))

    # text = 'failIfExecFails'
    #
    # start_time = time.time()
    # print(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', text))
    # print("--- %s seconds ---" % (time.time() - start_time))
    #
    # start_time = time.time()
    # print(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', text)).split())
    # print("--- %s seconds ---" % (time.time() - start_time))
    #
    # start_time = time.time()
    # print(re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', text))
    # print("--- %s seconds ---" % (time.time() - start_time))

    # text = 'bla_bla.bla@bla'

    # start_time = time.time()
    # print(re.split(r"[^\w\_]", text))
    # print("--- %s seconds ---" % (time.time() - start_time))
    #
    # start_time = time.time()
    # print(re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', text))
    # print("--- %s seconds ---" % (time.time() - start_time))
    #
    # start_time = time.time()
    # print(re.sub('[^0-9a-zA-Z]+', ' ', text))
    # print("--- %s seconds ---" % (time.time() - start_time))

    # code = 'private List<EJBDeploymentTool> deploymentTools = new ArrayList<>()'
    # tokens = Code_Tokenizer.get_tokenized_words(code, False, True)
    # print(tokens)

    lst1 = ['1','2','3']
    lst2 = ['3','4','5']
    lst3 = ["1 3", "2 2", "4 0", "5 7", "2 3", "2 1"]
    rez = []
    for esc in lst3:
        if any(any(term in esc for term in lst) for lst in (lst1, lst2)):
            rez.append(esc)

    print(rez)