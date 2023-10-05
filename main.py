import os
from datetime import datetime


def check_positive_int(number: str) -> int:
    if not number.isdigit():
        raise ValueError
    return int(number)


def random_generator_manager():
    choice = input("Please select input mode:\n1. Enter data\n2. Use config file\n")
    if choice == "1":
        try:
            m = check_positive_int(input("Enter m: "))
            a = check_positive_int(input("Enter a: "))
            c = check_positive_int(input("Enter c: "))
            x = check_positive_int(input("Enter x0: "))
            n = check_positive_int(input("Enter amount of random numbers(from 0 to m): "))
        except ValueError:
            print("Parameter for random generator should be positive integer")
            return 0
    elif choice == "2":
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
        print("Random numbers:")
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


while True:
    choice = input("Please choose action:\n0. Exit\n1. Clear console\n2. Generate random numbers\n")
    if choice == "0":
        print("Bye!")
        break
    if choice == "1":
        os.system("cls")
    elif choice == "2":
        from libs.random_number_generator import RandomNumberGenerator, get_period
        random_generator_manager()
    else:
        print("Wrong choice")
