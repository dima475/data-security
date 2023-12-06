from datetime import datetime

from libs.hash_generator import MD5HashGenerator
from libs.random_number_generator import RandomNumberGenerator
from libs.data_encryptor import RC5Encryptor, RC5Decryptor


def get_key(raw_key, length):
    key_hash = MD5HashGenerator.get_hash(raw_key.encode("utf-8"))
    if length == 8:
        return bytes.fromhex(key_hash)[:8]
    elif length == 16:
        return bytes.fromhex(key_hash)[:16]
    elif length == 32:
        res = b""
        res += bytes.fromhex(key_hash)[:16]
        new_key_hash = MD5HashGenerator.get_hash(key_hash.encode("utf-8"))
        res += bytes.fromhex(new_key_hash)[:16]
        return res


def get_first_iv(w):
    random_numbers = RandomNumberGenerator(2 ** 31 - 1, 48271, 0, int(datetime.now().timestamp()))
    iv = b""
    while len(iv) < w // 4:
        iv += next(random_numbers).to_bytes(4, byteorder="little")
    iv = iv[:w // 4]
    return iv


def remove_padding(decrypted_message):
    if len(decrypted_message) == 0:
        return decrypted_message
    padding_length = int(decrypted_message[-1])
    if padding_length > 0 and padding_length <= len(decrypted_message):
        return decrypted_message[:-padding_length]
    else:
        return decrypted_message


def encrypt_user_data(data: bytes, key: str, w, r, b):
    key = get_key(key, b)
    iv = get_first_iv(w)

    encryptor = RC5Encryptor(w, r, b, key, iv)
    res = encryptor.encrypt_data(data)
    return res.hex()


def decrypt_user_data(data: bytes, key: str, w, r, b):
    key = get_key(key, b)

    decryptor = RC5Decryptor(w, r, b, key)
    res = remove_padding(decryptor.decrypt_data(data))
    return res
