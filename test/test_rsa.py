import unittest
from libs.rsa import RSA

class TestRSAEncryption(unittest.TestCase):

    def setUp(self):
        self.passphrase = "secure_passphrase"
        self.data = b"Hello, World!"

    def test_key_generation(self):
        public_key, private_key = RSA.generate_keys(self.passphrase, 1024)
        self.assertIsNotNone(public_key)
        self.assertIsNotNone(private_key)

    def test_encryption_decryption(self):
        public_key, private_key = RSA.generate_keys(self.passphrase, 1024)

        encrypted_data = RSA.encrypt(self.data, public_key)
        self.assertIsNotNone(encrypted_data)

        decrypted_data = RSA.decrypt(encrypted_data, private_key, self.passphrase)
        self.assertEqual(decrypted_data, self.data)

    def test_encryption_with_invalid_public_key(self):
        invalid_public_key = b"invalid_key"
        encrypted_data = RSA.encrypt(self.data, invalid_public_key)
        self.assertIsNone(encrypted_data)

    def test_decryption_with_invalid_private_key(self):
        public_key, _ = RSA.generate_keys(self.passphrase, 1024)
        encrypted_data = RSA.encrypt(self.data, public_key)

        invalid_private_key = b"invalid_key"
        decrypted_data = RSA.decrypt(encrypted_data, invalid_private_key, self.passphrase)
        self.assertIsNone(decrypted_data)

    def test_decryption_with_wrong_passphrase(self):
        public_key, private_key = RSA.generate_keys(self.passphrase, 1024)
        encrypted_data = RSA.encrypt(self.data, public_key)

        wrong_passphrase = "wrong_passphrase"
        decrypted_data = RSA.decrypt(encrypted_data, private_key, wrong_passphrase)
        self.assertIsNone(decrypted_data)