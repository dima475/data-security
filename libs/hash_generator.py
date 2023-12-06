from math import floor, sin


class MD5HashGenerator:
    """
        This class provides a static method for generating MD5 hashes from input data.

        MD5 is a widely used cryptographic hash function that produces a 128-bit (16-byte)
        hash value from input data. The `get_hash` method of this class calculates the MD5
        hash of the provided bytes and returns it as a hexadecimal string.

        Attributes:
            None

        Methods:
            - get_hash(data: bytes) -> str: Computes the MD5 hash of the input data and
              returns it as a hexadecimal string.
    """

    @staticmethod
    def get_hash(data: bytes) -> str:
        """
            Compute the MD5 hash of the input data.

            Args:
                data (bytes): The input data for which the MD5 hash is calculated.

            Returns:
                str: The MD5 hash of the input data represented as a hexadecimal string.
        """

        # Step 0
        buffer = {
            "A": 0x67452301,
            "B": 0xEFCDAB89,
            "C": 0x98BADCFE,
            "D": 0x10325476
        }
        buffer_previous = buffer.copy()
        byte_string = bytearray(data)

        # Step 1
        byte_string.append(0x80)

        while len(byte_string) % 64 != 56:
            byte_string.append(0x00)

        # Step 2
        length = (len(data) * 8) % (2 ** 64)
        byte_string.extend(length.to_bytes(length=8, byteorder='little'))

        # Step 3
        F = lambda x, y, z: (x & y) | (~x & z)
        G = lambda x, y, z: (x & z) | (y & ~z)
        H = lambda x, y, z: x ^ y ^ z
        I = lambda x, y, z: y ^ (x | ~z)

        modular_add = lambda x, y: (x + y) % (2 ** 32)
        rotate_left = lambda x, n: (x << n) | (x >> (32 - n))

        S = [[7, 12, 17, 22],
             [5, 9, 14, 20],
             [4, 11, 16, 23],
             [6, 10, 15, 21]]

        T = [floor((2 ** 32) * abs(sin(i + 1))) for i in range(64)]

        for block_index in range(len(byte_string) // 64):
            X = [byte_string[block_index * 64 + i * 4:block_index * 64 + i * 4 + 4]
                 for i in range(16)]
            X = [int.from_bytes(x, byteorder="little") for x in X]

            for i in range(64):
                temp = None
                k = None
                if 0 <= i <= 15:
                    k = i
                    temp = F(buffer["B"], buffer["C"], buffer["D"])
                elif 16 <= i <= 31:
                    k = ((5 * i) + 1) % 16
                    temp = G(buffer["B"], buffer["C"], buffer["D"])
                elif 32 <= i <= 47:
                    k = ((3 * i) + 5) % 16
                    temp = H(buffer["B"], buffer["C"], buffer["D"])
                elif 48 <= i <= 63:
                    k = (7 * i) % 16
                    temp = I(buffer["B"], buffer["C"], buffer["D"])

                temp = modular_add(temp, buffer["A"])
                temp = modular_add(temp, X[k])
                temp = modular_add(temp, T[i])
                temp = rotate_left(temp, S[i // 16][i % 4])
                temp = modular_add(temp, buffer["B"])

                buffer["A"] = buffer["D"]
                buffer["D"] = buffer["C"]
                buffer["C"] = buffer["B"]
                buffer["B"] = temp

            buffer["A"] = modular_add(buffer["A"], buffer_previous["A"])
            buffer["B"] = modular_add(buffer["B"], buffer_previous["B"])
            buffer["C"] = modular_add(buffer["C"], buffer_previous["C"])
            buffer["D"] = modular_add(buffer["D"], buffer_previous["D"])
            buffer_previous = buffer.copy()

        return "".join(x.to_bytes(length=4, byteorder='little').hex() for x in buffer.values())
