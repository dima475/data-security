import oscrypto.asymmetric


class RSA:
    @staticmethod
    def generate_keys(passphrase, bits=1024):
        public_key, private_key = oscrypto.asymmetric.generate_pair('rsa', bit_size=bits)
        return oscrypto.asymmetric.dump_public_key(public_key), oscrypto.asymmetric.dump_private_key(private_key,
                                                                                                     passphrase)

    @staticmethod
    def encrypt(data, public_key):
        try:
            public_key = oscrypto.asymmetric.load_public_key(public_key)
            encrypted = b""
            for i in range(0, len(data), 11):
                encrypted_data = oscrypto.asymmetric.rsa_pkcs1v15_encrypt(public_key, data[i:i + 11])
                encrypted += encrypted_data
            return encrypted
        except:
            print("Error encrypting data")
            return None

    @staticmethod
    def decrypt(data, private_key, passphrase):
        try:
            private_key = oscrypto.asymmetric.load_private_key(private_key, passphrase)
            decrypted = b""
            for i in range(0, len(data), 128):
                decrypted_data = oscrypto.asymmetric.rsa_pkcs1v15_decrypt(private_key, data[i:i + 128])
                decrypted += decrypted_data
            return decrypted
        except:
            print("Error decrypting data")
            return None
