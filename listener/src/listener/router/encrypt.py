import time
import math
import random
import hashlib

KEY = "a2ffa5c9be07488bbb04a3a47d3c5f6a"

class Encrypt:
    def __init__(self, type, device_id ) -> None:
        self._type = type
        self._device_id = device_id
        self._time = math.floor(time.time())
        self._random = math.floor(random.random() * 10000)
    
    def get_none(self):
        return "_".join([str(self._type), self._device_id, str(self._time), str(self._random)])
    
    def encrypt(self, password, nonce):
        pass_str = f"{password}{KEY}"
        pass_hex = str(hashlib.sha1(pass_str.encode("utf-8")).hexdigest())
        enc_pass = str(hashlib.sha1((nonce + pass_hex).encode("utf-8")).hexdigest())
        return enc_pass

if __name__ == "__main__":
    enc = Encrypt(type=0, device_id="88:66:5a:24:46:db")
    nonce = enc.get_none()
    enc_pass = enc.encrypt("test", nonce=nonce)
    print(enc_pass)
    print(enc_pass == "9255e6d0e961698c3cfa4886ae602cd44c5b6967")