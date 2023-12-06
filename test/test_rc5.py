import time
import unittest
from libs.data_encryption import encrypt_user_data, decrypt_user_data, get_key, get_first_iv, remove_padding


class TestRC5Encryption(unittest.TestCase):

    def setUp(self):
        self.test_data = b"Hello, World!"
        self.keys = ["short_key", "a_medium_length_key", "a_very_long_key_to_test_different_key_sizes"]
        self.parameters = [(32, 12, 8), (64, 16, 16), (16, 20, 32)]

    def test_encryption_decryption(self):
        for key in self.keys:
            for w, r, b in self.parameters:
                with self.subTest(key=key, w=w, r=r, b=b):
                    encrypted_data = encrypt_user_data(self.test_data, key, w, r, b)
                    decrypted_data = decrypt_user_data(bytes.fromhex(encrypted_data), key, w, r, b)
                    self.assertEqual(self.test_data, decrypted_data)

    def test_key_derivation(self):
        for key in self.keys:
            for length in [8, 16, 32]:
                with self.subTest(key=key, length=length):
                    derived_key = get_key(key, length)
                    self.assertEqual(len(derived_key), length)

    def test_iv_generation(self):
        for w, r, b in self.parameters:
            with self.subTest(w=w, r=r, b=b):
                iv = get_first_iv(w)
                self.assertEqual(len(iv), w // 4)

    def test_remove_padding(self):
        padded_data = self.test_data + (4 * b'\x04')
        self.assertEqual(remove_padding(padded_data), self.test_data)

    def test_different_ivs_produce_different_ciphertexts(self):
        key = "test_key"
        w, r, b = 32, 12, 16
        encrypted_data1 = encrypt_user_data(self.test_data, key, w, r, b)
        time.sleep(1)
        encrypted_data2 = encrypt_user_data(self.test_data, key, w, r, b)
        self.assertNotEqual(encrypted_data1, encrypted_data2)

    def test_incorrect_key_for_decryption(self):
        key = "correct_key"
        wrong_key = "wrong_key"
        w, r, b = 32, 12, 16
        encrypted_data = encrypt_user_data(self.test_data, key, w, r, b)
        decrypted_data = decrypt_user_data(bytes.fromhex(encrypted_data), wrong_key, w, r, b)
        self.assertNotEqual(self.test_data, decrypted_data)

    def test_empty_string_encryption(self):
        key = "test_key"
        w, r, b = 32, 12, 16
        encrypted_data = encrypt_user_data(b"", key, w, r, b)
        decrypted_data = decrypt_user_data(bytes.fromhex(encrypted_data), key, w, r, b)
        self.assertEqual(b"", decrypted_data)

    def test_long_string_encryption(self):
        key = "test_key"
        w, r, b = 64, 12, 32
        long_data = b"a" * 1000
        encrypted_data = encrypt_user_data(long_data, key, w, r, b)
        decrypted_data = decrypt_user_data(bytes.fromhex(encrypted_data), key, w, r, b)
        self.assertEqual(long_data, decrypted_data)