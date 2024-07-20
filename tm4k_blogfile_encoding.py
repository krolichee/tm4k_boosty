import json
import os.path
import re

def getStringWithDecodedUnicode( value ):
    findUnicodeRE = re.compile( '\\\\u([\da-f]{4})' )
    def getParsedUnicode(x):
        return chr( int( x.group(1), 16 ) )
    return  findUnicodeRE.sub(getParsedUnicode, str( value ) )
file1 = open("posts.boosty","r")
lst = json.loads(file1.read())
open_method = "w" if os.path.isfile("posts1.boosty") else "x"
file2 = open("posts1.boosty",open_method)
file2.write(getStringWithDecodedUnicode(file1.read()))
