from dataclasses import dataclass


@dataclass
class RC5:
    w: int
    r: int
    b: int
    key: bytes
    iv: bytes = None

    def _modular_add(self, x: int, y: int) -> int:
        return (x + y) % (2 ** self.w)

    def _rotate_left(self, x: int, n: int) -> int:
        mask = 2 ** self.w - 1
        n %= self.w
        return ((x << n) & mask) | ((x & mask) >> (self.w - n))

    def _modular_sub(self, x: int, y: int) -> int:
        return (x - y) % (2 ** self.w)

    def _rotate_right(self, x: int, n: int) -> int:
        mask = 2 ** self.w - 1
        n %= self.w
        return ((x & mask) >> n) | (x << (self.w - n) & mask)

    def __const_for_key(self):
        if self.w == 16:
            return (0xB7E1, 0x9E37)
        elif self.w == 32:
            return (0xB7E15163, 0x9E3779B9)
        elif self.w == 64:
            return (0xB7E151628AED2A6B, 0x9E3779B97F4A7C15)

    def _get_keys(self):
        u = self.w // 8

        if self.b == 0:
            c = 1
        elif self.b % (self.w // 8):
            self.key += b'\x00' * ((self.w // 8) - self.b % (self.w // 8))
            self.b = len(self.key)
            c = self.b // u
        else:
            c = self.b // u

        L = [0] * c
        for i in range(self.b - 1, -1, -1):
            L[i // u] = (L[i // u] << 8) + self.key[i]

        P, Q = self.__const_for_key()
        S = []
        S.append(P)
        for i in range(1, 2 * self.r + 2):
            S.append(self._modular_add(S[i - 1], Q))

        i, j, A, B = 0, 0, 0, 0
        for k in range(3 * max(c, 2 * self.r + 2)):
            A = S[i] = self._rotate_left((S[i] + A + B), 3)
            B = L[j] = self._rotate_left((L[j] + A + B), A + B)
            i = (i + 1) % (2 * self.r + 2)
            j = (j + 1) % c

        return S


class RC5Encryptor(RC5):
    def encrypt_block(self, block: bytes):
        S = self._get_keys()

        A = int.from_bytes(block[:self.w // 8], byteorder="little")
        B = int.from_bytes(block[self.w // 8:], byteorder="little")

        A = self._modular_add(A, S[0])
        B = self._modular_add(B, S[1])

        for i in range(1, self.r + 1):
            A = self._modular_add(self._rotate_left((A ^ B), B), S[2 * i])
            B = self._modular_add(self._rotate_left((A ^ B), A), S[2 * i + 1])

        return (A.to_bytes(self.w // 8, byteorder='little') + B.to_bytes(self.w // 8, byteorder='little'))

    def encrypt_data(self, data):
        w4 = self.w // 4
        encrypted_data = b''
        encrypted_data += self.encrypt_block(self.iv)
        last_block = self.iv
        for i in range(0, len(data), w4):
            data_block_raw = data[i:i + w4]

            if len(data_block_raw) < w4:
                data_block_raw += (w4 - len(data_block_raw)).to_bytes(1) * (w4 - len(data_block_raw))
            else:
                data_block_raw += w4.to_bytes(1) * w4

            data_block = bytes([a ^ b for a, b in zip(last_block, data_block_raw)])
            last_block = self.encrypt_block(data_block)

            encrypted_data += last_block
        return encrypted_data


class RC5Decryptor(RC5):
    def decrypt_block(self, block: bytes):
        S = self._get_keys()

        A = int.from_bytes(block[:self.w // 8], byteorder="little")
        B = int.from_bytes(block[self.w // 8:], byteorder="little")

        for i in range(self.r, 0, -1):
            B = self._rotate_right(B - S[2 * i + 1], A) ^ A
            A = self._rotate_right(A - S[2 * i], B) ^ B

        B = self._modular_sub(B, S[1])
        A = self._modular_sub(A, S[0])

        return (A.to_bytes(self.w // 8, byteorder='little') + B.to_bytes(self.w // 8, byteorder='little'))

    def decrypt_data(self, data):

        w4 = self.w // 4
        decrypted_data = b''
        last_block = self.decrypt_block(data[:w4])
        for i in range(w4, len(data), w4):
            data_block = data[i:i + w4]
            decrypted_block = self.decrypt_block(data_block)
            decrypted_block = bytes([a ^ b for a, b in zip(last_block, decrypted_block)])
            last_block = data_block
            decrypted_data += decrypted_block
        return decrypted_data
