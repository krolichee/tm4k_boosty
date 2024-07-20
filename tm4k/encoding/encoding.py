import re


def getStringWithDecodedUnicode(value):
    find_unicode_re = re.compile('\\\\u([\da-f]{4})')

    def getParsedUnicode(x):
        return chr(int(x.group(1), 16))

    return find_unicode_re.sub(getParsedUnicode, str(value))
