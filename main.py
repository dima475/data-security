import os
from datetime import datetime
import toml


def check_positive_int(number: str) -> int:
    if not number.isdigit():
        raise ValueError
    return int(number)


def random_generator_manager(is_config):
    mode = input("Please select input mode:\n"
                 "1. Enter data\n"
                 "2. Use config file\n")

    if mode == "1":
        try:
            m = check_positive_int(input("Please enter m: "))
            a = check_positive_int(input("Please enter a: "))
            c = check_positive_int(input("Please enter c: "))
            x = check_positive_int(input("Please enter x0: "))
            n = check_positive_int(input("Please enter amount of random numbers(from 0 to m): "))
        except ValueError:
            print("Parameter for random generator should be a positive integer")
            return 0
    elif mode == "2":
        if is_config:
            with open("config.toml", "r") as toml_file:
                config = toml.load(toml_file)
            data = config.get("random_numbers", {})
            m = data.get("m")
            a = data.get("a")
            c = data.get("c")
            x = data.get("x")
            n = data.get("n")
        else:
            from config import m, a, c, x, n
    else:
        print("Wrong mode selected")
        return 0

    write_to_file = input("Write random numbers to file? (y/n): ")
    write_to_console = input("Write random numbers to console? (y/n): ")

    if write_to_console != "y" and write_to_file != "y":
        print("Nothing to do")
        return 0

    file = open(f'result_data/random_numbers_{datetime.now().strftime("%Y%m%d-%H%M%S")}.txt', 'w',
                encoding="utf-8") if write_to_file == "y" else None

    random_generator = RandomNumberGenerator(m, a, c, x)

    if write_to_console == "y":
        print("\nRandom numbers:")
        print(x, end=" ")
    if file:
        file.write(str(x) + " ")

    for _ in range(n):
        number = next(random_generator)
        if write_to_console == "y":
            print(number, end=" ")
        if file:
            file.write(str(number) + " ")
    if file:
        file.close()

    period: int = get_period(m, a, c, x)
    print(f"\nPeriod of sequence = {period}")
    return 0


def hash_generator_manager(is_config):
    data_to_hash = []
    mode = input("Please select input mode:\n"
                 "1. Enter one string\n"
                 "2. Enter many strings\n"
                 "3. Use config file\n"
                 "4. Use data from file\n"
                 "5. Verify file integrity\n")

    if mode == "1":
        data_to_hash.append(input("Please enter string: "))
    elif mode == "2":
        try:
            n = check_positive_int(input("Please enter amount of strings: "))
        except ValueError:
            print("Amount of strings should be a positive integer")
            return 0
        for _ in range(n):
            data_to_hash.append(input("Please enter string: "))
    elif mode == "3":
        if is_config:
            with open("config.toml", "r") as toml_file:
                config = toml.load(toml_file)
            data = config.get("hash", {})
            data_to_hash = data.get("data_to_hash")
        else:
            from config import data_to_hash
    elif mode == "4":
        file_name = input("Please enter file name(maximum file size is 5 MB): ")
        try:
            if os.path.getsize(file_name) > 5242880:
                print("File is bigger than 5 MB")
                return 0

            with open(file_name, "rb") as file:
                data_to_hash.append(file.read())
        except FileNotFoundError:
            print("File not found")
            return 0
    elif mode == "5":
        file_name = input("Please enter file name(maximum file size is 5 MB): ")
        try:
            if os.path.getsize(file_name) > 5242880:
                print("File is bigger than 5 MB")
                return 0

            with open(file_name, "rb") as file:
                data = file.read()
        except FileNotFoundError:
            print("File not found")
            return 0
        file_hash = input("Please enter MD5 hash: ")
        hash_result = MD5HashGenerator.get_hash(data)
        if hash_result == file_hash:
            print("File integrity verified")
        else:
            print("File integrity not verified")
        return 0
    else:
        print("Wrong mode selected")
        return 0

    write_to_file = input("Write hash to file? (y/n): ")
    write_to_console = input("Write hash to console? (y/n): ")

    if write_to_console != "y" and write_to_file != "y":
        print("Nothing to do")
        return 0

    if write_to_console == "y":
        print("\nHash:")

    file = open(f'result_data/hash_{datetime.now().strftime("%Y%m%d-%H%M%S")}.txt', 'w',
                encoding="utf-8") if write_to_file == "y" else None

    for data in data_to_hash:
        if mode == "4":
            hash_result = MD5HashGenerator.get_hash(data)
            data = "file data"
        else:
            hash_result = MD5HashGenerator.get_hash(data.encode("utf-8"))

        if write_to_console == "y":
            print(f"{data} -> {hash_result}")
        if write_to_file == "y":
            file.write(hash_result + "\n")
    if file:
        file.close()
    return 0


def encryption_manager(is_config):
    mode_parameters = input("Please select input mode for encryption|decryption parameters:\n"
                            "1. Enter data\n"
                            "2. Use config file\n")

    if mode_parameters == "1":
        try:
            w = check_positive_int(input("Please enter w(word size in bits(16, 32, 64)): "))
            if w not in [16, 32, 64]:
                print("Word size should be 16, 32 or 64")
                return 0
            r = check_positive_int(input("Please enter r(number of rounds): "))
            b = check_positive_int(input("Please enter b(key size in bytes(8, 16, 32)): "))
            if b not in [8, 16, 32]:
                print("Key size should be 8, 16 or 32")
                return 0
        except ValueError:
            print("Parameter for encryption should be a positive integer")
            return 0
    elif mode_parameters == "2":
        if is_config:
            with open("config.toml", "r") as toml_file:
                config = toml.load(toml_file)
            data = config.get("encryption", {})
            w = data.get("w")
            r = data.get("r")
            b = data.get("b")
        else:
            from config import w, r, b
    else:
        print("Wrong mode for input parameters selected")
        return 0

    mode_data = input("Please select input mode for data:\n"
                      "1. Enter data\n"
                      "2. Use data from file\n")

    if mode_data == "1":
        data = input("Please enter string: ").encode("utf-8")
        key = input("Please enter key: ")
    elif mode_data == "2":
        file_name = input("Please enter file name(maximum file size is 5 MB): ")
        try:
            if os.path.getsize(file_name) > 5242880:
                print("File is bigger than 5 MB")
                return 0

            with open(file_name, "rb") as file:
                data = file.read()
        except FileNotFoundError:
            print("File not found")
            return 0
        key = input("Please enter key: ")
    else:
        print("Wrong mode for input data selected")
        return 0

    mode = input("Please select work mode:\n"
                 "1. Encrypt data\n"
                 "2. Decrypt data\n")

    if mode == "1":
        res = encrypt_user_data(data, key, w, r, b)
    elif mode == "2":
        data_to_decrypt = bytes.fromhex(data.decode("utf-8"))
        res = decrypt_user_data(data_to_decrypt, key, w, r, b)
        decode_result = input("Decode result to utf-8? (y/n): ")
        try:
            if decode_result == "y":
                res = res.decode("utf-8")
        except:
            print("Error while decoding")

    else:
        print("Wrong work mode selected")
        return 0

    write_to_file = input("Write result to file? (y/n): ")
    write_to_console = input("Write result to console? (y/n): ")

    if write_to_console != "y" and write_to_file != "y":
        print("Nothing to do")
        return 0

    if write_to_console == "y":
        print("\nResult:")
        print(f"{data} -> {res}")

    if write_to_file == "y":
        format = "txt"
        if mode == "2":
            format = input("Please enter result_file format: ")

        if format in ["txt"]:
            mode_save = "w"
        else:
            mode_save = "wb"

        with open(
                f'result_data/{"encryption" if mode == "1" else "decryption"}_{datetime.now().strftime("%Y%m%d-%H%M%S")}.{format}',
                mode_save) as file:
            file.write(res)
    return 0


def generate_save_key_pair(algorithm):
    passphrase = input("Please enter private key passphrase: ")

    if algorithm == "rsa":
        public_key, private_key = RSA.generate_keys(passphrase)

        with open(
                f'result_data/public_rsa_key_{datetime.now().strftime("%Y%m%d-%H%M%S")}.txt',
                "wb") as file:
            file.write(public_key)
        with open(
                f'result_data/private_rsa_key_{datetime.now().strftime("%Y%m%d-%H%M%S")}.txt',
                "wb") as file:
            file.write(private_key)
        print("Keys generated and saved successfully")
        return public_key
    elif algorithm == "dsa":
        public_key, private_key = DSA.generate_keys(passphrase)

        with open(
                f'result_data/public_dsa_key_{datetime.now().strftime("%Y%m%d-%H%M%S")}.txt',
                "wb") as file:
            file.write(public_key)
        with open(
                f'result_data/private_dsa_key_{datetime.now().strftime("%Y%m%d-%H%M%S")}.txt',
                "wb") as file:
            file.write(private_key)
        print("Keys generated and saved successfully")
        return private_key, passphrase
    else:
        print("Wrong algorithm selected")
        return 0


def rsa_encryption_manager(is_config):
    mode = input("Please select work mode:\n"
                 "1. Encrypt data\n"
                 "2. Decrypt data\n"
                 "3. Generate key pair\n")
    if mode in ["1", "2"]:
        mode_data = input("Please select input mode for data:\n"
                          "1. Enter data\n"
                          "2. Use data from file\n"
                          "3. Use data from config file\n")

        if mode_data == "1":
            data_to_encrypt = input("Please enter string: ").encode("utf-8")
        elif mode_data == "2":
            file_name = input("Please enter file name(maximum file size is 5 MB): ")
            try:
                if os.path.getsize(file_name) > 5242880:
                    print("File is bigger than 5 MB")
                    return 0

                with open(file_name, "rb") as file:
                    data_to_encrypt = file.read()
            except FileNotFoundError:
                print("File not found")
                return 0
        elif mode_data == "3":
            if is_config:
                with open("config.toml", "r") as toml_file:
                    config = toml.load(toml_file)
                config_data = config.get("rsa_encryption", {})
                data_to_encrypt = config_data.get("data_to_encrypt").encode("utf-8")
            else:
                from config import data_to_encrypt
        else:
            print("Wrong mode for input data selected")
            return 0

        if mode == "1":
            key_mode = input("Please select key mode:\n"
                             "1. Use key from file\n"
                             "2. Generate key pair\n")
        else:
            key_mode = "1"

        if key_mode == "1":
            file_name = input(f'Please enter name of file with {"public" if mode == "1" else "private"} key: ')
            try:
                with open(file_name, "rb") as file:
                    key = file.read()
            except FileNotFoundError:
                print("File not found")
                return 0
            if mode == "2":
                passphrase = input("Please enter private key passphrase: ")

        elif key_mode == "2" and mode == "1":
            key = generate_save_key_pair(algorithm="rsa")
        else:
            print("Wrong key mode selected")
            return 0

        if mode == "1":
            res = RSA.encrypt(data_to_encrypt, key)
            if res == None:
                return 0
        elif mode == "2":
            res = RSA.decrypt(data_to_encrypt, key, passphrase)
            if res == None:
                return 0
            decode_result = input("Decode result to utf-8? (y/n): ")
            try:
                if decode_result == "y":
                    res = res.decode("utf-8")
            except:
                print("Error while decoding")

        write_to_file = input("Write result to file? (y/n): ")
        write_to_console = input("Write result to console? (y/n): ")

        if write_to_console != "y" and write_to_file != "y":
            print("Nothing to do")
            return 0

        if write_to_console == "y":
            print("\nResult:")
            print(f"{data_to_encrypt} -> {res}")

        if write_to_file == "y":
            format = input("Please enter result_file format: ")
            if type(res) == str:
                res = res.encode("utf-8")

            with open(
                    f'result_data/{"rsa_encryption" if mode == "1" else "rsa_decryption"}_{datetime.now().strftime("%Y%m%d-%H%M%S")}.{format}',
                    "wb") as file:
                file.write(res)
        return 0
    elif mode == "3":
        generate_save_key_pair(algorithm="rsa")
        return 0
    else:
        print("Wrong work mode selected")
        return 0


def dsa_manager(is_config):
    mode = input("Please select work mode:\n"
                 "1. Sign data\n"
                 "2. Verify data\n"
                 "3. Generate key pair\n")
    if mode in ["1", "2"]:
        mode_data = input("Please select input mode for data:\n"
                          "1. Enter data\n"
                          "2. Use data from file\n"
                          "3. Use data from config file\n")

        if mode_data == "1":
            data = input("Please enter string: ").encode("utf-8")
        elif mode_data == "2":
            file_name = input("Please enter file name(maximum file size is 5 MB): ")
            try:
                if os.path.getsize(file_name) > 5242880:
                    print("File is bigger than 5 MB")
                    return 0

                with open(file_name, "rb") as file:
                    data = file.read()
            except FileNotFoundError:
                print("File not found")
                return 0
        elif mode_data == "3":
            if is_config:
                with open("config.toml", "r") as toml_file:
                    config = toml.load(toml_file)
                config_data = config.get("dsa_sign", {})
                data = config_data.get("data_to_sign").encode("utf-8")
            else:
                from config import data_to_sign as data
        else:
            print("Wrong mode for input data selected")
            return 0

        if mode == "1":
            key_mode = input("Please select key mode:\n"
                             "1. Use key from file\n"
                             "2. Generate key pair\n")
        else:
            key_mode = "1"

        if key_mode == "1":
            file_name = input(f'Please enter name of file with {"private" if mode == "1" else "public"} key: ')
            try:
                with open(file_name, "rb") as file:
                    key = file.read()
            except FileNotFoundError:
                print("File not found")
                return 0
            if mode == "1":
                passphrase = input("Please enter private key passphrase: ")

        elif key_mode == "2" and mode == "1":
            key, passphrase = generate_save_key_pair(algorithm="dsa")
        else:
            print("Wrong key mode selected")
            return 0

        if mode == "1":
            print("Please wait...\n")
            res = DSA.sign(data, key, passphrase)
            if res == None:
                return 0
        elif mode == "2":
            sign_file = input("Please enter file with signature: ")
            try:
                with open(sign_file, "rb") as file:
                    signature = file.read()
            except FileNotFoundError:
                print("File not found")
                return 0
            print("Please wait...\n")
            res = DSA.verify(data, signature, key)
            if res == None:
                return 0

        write_to_file = input("Write result to file? (y/n): ")
        write_to_console = input("Write result to console? (y/n): ")

        if write_to_console != "y" and write_to_file != "y":
            print("Nothing to do")
            return 0

        if write_to_console == "y":
            print("\nResult:")
            print(res)

        if write_to_file == "y":
            if type(res) == str:
                res = res.encode("utf-8")
            with open(
                    f'result_data/{"dsa_signature" if mode == "1" else "dsa_verification"}_{datetime.now().strftime("%Y%m%d-%H%M%S")}.txt',
                    "wb") as file:
                file.write(res)
        return 0
    elif mode == "3":
        generate_save_key_pair(algorithm="dsa")
        return 0
    else:
        print("Wrong work mode selected")
        return 0


if not os.path.exists("result_data"):
    os.mkdir("result_data")

if os.path.exists("config.toml"):
    is_config = 1
else:
    is_config = 0
    print("Warning: No configuration file")

while True:
    choice = input("Please choose action:\n"
                   "0. Exit\n"
                   "1. Clear console\n"
                   "2. Generate random numbers\n"
                   "3. Generate MD5 hash\n"
                   "4. Encrypt data\n"
                   "5. RSA encryption\n"
                   "6. DSA signature\n")
    if choice == "0":
        print("Bye!")
        break
    if choice == "1":
        os.system("cls")
    elif choice == "2":
        from libs.random_number_generator import RandomNumberGenerator, get_period

        random_generator_manager(is_config)
        print()
    elif choice == "3":
        from libs.hash_generator import MD5HashGenerator

        hash_generator_manager(is_config)
        print()
    elif choice == "4":
        from libs.data_encryption import encrypt_user_data, decrypt_user_data

        encryption_manager(is_config)
        print()
    elif choice == "5":
        from libs.rsa import RSA

        rsa_encryption_manager(is_config)
        print()
    elif choice == "6":
        from libs.dsa import DSA

        dsa_manager(is_config)
        print()
    else:
        print("Wrong choice")
