import oscrypto.asymmetric


class DSA:
    @staticmethod
    def generate_keys(passphrase, bits=2048):
        public_key, private_key = oscrypto.asymmetric.generate_pair('dsa', bit_size=bits)
        return oscrypto.asymmetric.dump_public_key(public_key), oscrypto.asymmetric.dump_private_key(private_key,
                                                                                                     passphrase)

    @staticmethod
    def sign(data, private_key, passphrase, hash_algorithm="sha256"):
        try:
            private_key_loaded = oscrypto.asymmetric.load_private_key(private_key, passphrase)
            signature = oscrypto.asymmetric.dsa_sign(private_key_loaded, data, hash_algorithm)
            return signature
        except:
            print("\nError signing data")
            return None

    @staticmethod
    def verify(data, signature, public_key, hash_algorithm="sha256"):
        try:
            public_key = oscrypto.asymmetric.load_public_key(public_key)
            oscrypto.asymmetric.dsa_verify(public_key, signature, data, hash_algorithm)
            return 'Data is verified'
        except:
            print("\nData is not verified")
            return None
