"""
Author: @oriapp 
"""
from cipher import Cipher
import hashlib

class sha256(Cipher):

    name = 'sha256'
    type = 'hash function'

    @staticmethod
    def encode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        output = hashlib.sha256( text.encode('ascii') ).hexdigest()

        return {'text': output, 'success': True}

    @staticmethod
    def print_options():
        print(''' 
        ### Modes
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text

        ### Examples
        python main.py sha256 -e -t 'hello'
        ''')
