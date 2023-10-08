import os
from datetime import datetime


def check_positive_int(number: str) -> int:
    if not number.isdigit():
        raise ValueError
    return int(number)


def random_generator_manager():
    mode = input("Please select input mode:\n"
                 "1. Enter data\n"
                 "2. Use config file\n")

    if mode == "1":
        try:
            m = check_positive_int(input("Enter m: "))
            a = check_positive_int(input("Enter a: "))
            c = check_positive_int(input("Enter c: "))
            x = check_positive_int(input("Enter x0: "))
            n = check_positive_int(input("Enter amount of random numbers(from 0 to m): "))
        except ValueError:
            print("Parameter for random generator should be a positive integer")
            return 0
    elif mode == "2":
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


def hash_generator_manager():
    strings_to_hash = []
    mode = input("Please select input mode:\n"
                 "1. Enter one string\n"
                 "2. Enter many strings\n"
                 "3. Use config file\n")

    if mode == "1":
        strings_to_hash.append(input("Enter string: "))
    elif mode == "2":
        try:
            n = check_positive_int(input("Enter amount of strings: "))
        except ValueError:
            print("Amount of strings should be a positive integer")
            return 0
        for _ in range(n):
            strings_to_hash.append(input("Enter string: "))
    elif mode == "3":
        from config import strings_to_hash
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

    for string in strings_to_hash:
        hash_result = MD5HashGenerator.get_hash(string)
        if write_to_console == "y":
            print(f"{string} -> {hash_result}")
        if write_to_file == "y":
            file.write(hash_result + "\n")
    if file:
        file.close()
    return 0


while True:
    choice = input("Please choose action:\n"
                   "0. Exit\n"
                   "1. Clear console\n"
                   "2. Generate random numbers\n"
                   "3. Generate hash\n")
    if choice == "0":
        print("Bye!")
        break
    if choice == "1":
        os.system("cls")
    elif choice == "2":
        from libs.random_number_generator import RandomNumberGenerator, get_period

        random_generator_manager()
        print()
    elif choice == "3":
        from libs.hash_generator import MD5HashGenerator

        hash_generator_manager()
        print()
    else:
        print("Wrong choice")
