import random
import string

DEFAULT_CHAR_STRING = string.ascii_lowercase + string.digits


def generate_random_string(chars=DEFAULT_CHAR_STRING, size=6):
    return "".join(random.choice(chars) for _ in range(size))


def count_numbers():
    a = "a"
    if a == "b":
        a = 2
    elif a == "a":
        a = 1
    else:
        a = 3

    total = 0
    total += 1
    total += 2
    total += 3
    total += a
    return total


def count_others():
    a = "a"
    if a == "b":
        a = 2
    elif a == "a":
        a = 1
    else:
        a = 3
    return a
