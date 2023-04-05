

def id_str_to_set(strings, sep=','):
    result = set()
    strings = strings + sep
    length = len(strings)
    index = 0
    for i in range(length):
        if strings[i] != sep:
            continue
        val_str = strings[index:i].strip()
        if val_str.isdigit():
            result.add(int(val_str))
        index = i + 1
    return result
