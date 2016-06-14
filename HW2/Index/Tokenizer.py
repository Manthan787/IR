import re
from Encoder import DeltaEncoder
import sys
import json


class Tokenizer( object ):


    def __init__(self, text):
        self.text   = text


    def __findTokens(self, text):
        tokenPattern = re.compile('([0-9a-z]+(\.?[0-9a-z]+)*)')
        return [t[0] for t in tokenPattern.findall(text.lower())]


    def tokenize(self):
            return self.__findTokens(self.text)
