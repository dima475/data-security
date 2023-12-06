import unittest
from libs.dsa import DSA

class TestDSASignature(unittest.TestCase):

    def setUp(self):
        self.passphrase = "secure_passphrase"
        self.data = b"Hello, World!"

    def test_key_generation(self):
        public_key, private_key = DSA.generate_keys(self.passphrase, 2048)
        self.assertIsNotNone(public_key)
        self.assertIsNotNone(private_key)

    def test_sign_and_verify(self):
        public_key, private_key = DSA.generate_keys(self.passphrase, 2048)

        signature = DSA.sign(self.data, private_key, self.passphrase)
        self.assertIsNotNone(signature)

        verification_result = DSA.verify(self.data, signature, public_key)
        self.assertEqual(verification_result, 'Data is verified')

    def test_sign_with_invalid_private_key(self):
        invalid_private_key = b"invalid_key"
        signature = DSA.sign(self.data, invalid_private_key, self.passphrase)
        self.assertIsNone(signature)

    def test_verify_with_invalid_public_key(self):
        public_key, private_key = DSA.generate_keys(self.passphrase, 2048)
        signature = DSA.sign(self.data, private_key, self.passphrase)

        invalid_public_key = b"invalid_key"
        verification_result = DSA.verify(self.data, signature, invalid_public_key)
        self.assertIsNone(verification_result)

    def test_verify_with_wrong_data(self):
        public_key, private_key = DSA.generate_keys(self.passphrase, 2048)
        signature = DSA.sign(self.data, private_key, self.passphrase)

        wrong_data = b"Incorrect data"
        verification_result = DSA.verify(wrong_data, signature, public_key)
        self.assertIsNone(verification_result)

    def test_verify_with_wrong_signature(self):
        public_key, private_key = DSA.generate_keys(self.passphrase, 2048)
        DSA.sign(self.data, private_key, self.passphrase)

        wrong_signature = b"Incorrect signature"
        verification_result = DSA.verify(self.data, wrong_signature, public_key)
        self.assertIsNone(verification_result)