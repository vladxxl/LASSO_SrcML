import re
import subprocess
from enum import Enum
from bs4 import BeautifulSoup
import javalang
import sctokenizer

tokenize_xpath = [
    "//src:name[not(ancestor::src:type)]/child::text() | //src:literal/child::text()",
    "//src:name/child::text() | //src:literal/child::text()"
]

JAVA_KEYWORDS = ["abstract", "continue", "for", "new", "switch",
                 "assert", "default", "if", "package", "synchronized",
                 "boolean", "do", "goto", "private", "this",
                 "break", "double", "implements", "protected", "throw",
                 "byte", "else", "import", "public", "throws",
                 "case", "enum", "instanceof", "return", "transient",
                 "catch", "extends", "int", "short", "try",
                 "char", "final", "interface", "static", "void",
                 "class", "finally", "long", "strictfp", "volatile",
                 "const", "float", "native", "super", "while",
                 "", "String", "List"]

COMMON_VARIABLES = ['i', 'j', 'k', 'm', 'n', 'c', 'd', 'e', 'a', 'x']


def apply_java_tokens_exclusion(text):
    return [word for word in text if word not in JAVA_KEYWORDS]


def apply_common_variables_exclusion(text):
    return [word for word in text if word not in COMMON_VARIABLES]


def apply_special_characters_flag(text):
    return re.sub('[^0-9a-zA-Z]+', ' ', text).strip()


def apply_camel_case_flag(text):
    return re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', text)


class TokenType(Enum):
    integer = 1
    float = 2
    bool = 3
    string = 4


# note: order is important! most generic patterns always go to the bottom
scanner = re.Scanner([
    (r"\d+\.\d*", lambda s, t: (TokenType.float, float(t))),
    (r"\d+", lambda s, t: (TokenType.integer, int(t))),
    (r"true|false+", lambda s, t: (TokenType.bool, t == "true")),
    (r"'[^']+'", lambda s, t: (TokenType.string, t[1:-1])),
    (r"\w+", lambda s, t: (TokenType.string, t)),
    (r".", lambda s, t: None),  # ignore unmatched parts
])


def get_tokenized_words(code, special_characters_flag, camel_case_flag):
    result_tokens = []

    # eliminate extra spaces and \n, \t
    code = " ".join(code.split())

    # "unknown" contains unmatched text, check it for error handling
    tokens, unknown = scanner.scan(code.lower())

    for t_type, t_val in tokens:
        result_tokens.append(str(t_val))

    # split words by the special characters
    if special_characters_flag:
        for elem in apply_special_characters_flag(code).split():
            if elem.lower() not in result_tokens:
                result_tokens.append(elem.lower())

    # split words by the camel case
    if camel_case_flag:
        for elem in apply_camel_case_flag(code):
            if elem.lower() not in result_tokens:
                result_tokens.append(elem.lower())

    # handle for tokens that contain "_" to be added to the token list with and without "_"
    for c in result_tokens:
        if "_" in c:
            result_tokens.append(re.sub('[_]+', '', c))

    # exclude java tokens from the code
    result_tokens = apply_java_tokens_exclusion(result_tokens)
    # exclude common names for temporary variables from the code
    # result_tokens = apply_common_variables_exclusion(result_tokens)

    return result_tokens


def get_tokenized_words2(code, tokenize_option, special_characters_flag, language):
    result_tokens = []

    # apply srcML to tokenize the code
    srcML = subprocess.Popen(["srcml", "--xpath", tokenize_xpath[tokenize_option], "-t", code, "-l", language],
                             stdout=subprocess.PIPE)
    output = srcML.communicate()[0]

    # use BeautifulSoup to parse the result of the XPath queries
    soup = BeautifulSoup(output, 'xml')
    names = soup.find_all('unit', item=True)
    for name in names:
        result_tokens.append(apply_special_characters_flag(name.text, special_characters_flag))

    return result_tokens


def get_tokenized_words3(code, tokenize_option, special_characters_flag, language):
    result_tokens = []

    print(code)
    if code:
        tokens = list(javalang.tokenizer.tokenize(code))
        for token in tokens:
            if len(token.value) != "" and token.value not in JAVA_KEYWORDS:
                result_tokens.append(apply_special_characters_flag(token.value.lower(), special_characters_flag))

    return result_tokens


def get_tokenized_words4(code, tokenize_option, special_characters_flag, language):
    result_tokens = []

    tokens = sctokenizer.tokenize_str(code, lang='java')
    for token in tokens:
        if token.token_value != "" and token.token_value not in JAVA_KEYWORDS:
            result_tokens.append(apply_special_characters_flag(token.token_value.lower(), special_characters_flag))

    return result_tokens