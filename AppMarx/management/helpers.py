import random
import string


# self explanatory

def make_random_string(length):
    return "".join(random.sample(string.letters+string.digits, length))

# access dict values safely(no exception)

def safe_dict_get(dict, key):
    try:
        value = dict[key]
    except KeyError:
        return None
    return value

def in_list(list, value):
    try:
        i = list.index(value)
    except ValueError:
        return None
    return i+1