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
                   "3. Generate MD5 hash\n")
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
    else:
        print("Wrong choice")
