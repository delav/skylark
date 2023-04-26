

def id_str_to_set(strings, sep=',', to_int=False):
    result = set()
    strings = strings + sep
    length = len(strings)
    index = 0
    for i in range(length):
        if strings[i] != sep:
            continue
        val_str = strings[index:i].strip()
        if val_str.isdigit():
            val_str = int(val_str) if to_int else val_str
            result.add(val_str)
        index = i + 1
    return result


def join_id_to_str(id_iter, sep=','):
    result = ''
    length = len(id_iter)
    for i in range(length):
        if i != length - 1:
            result += str(id_iter[i]) + sep
            continue
        result += str(id_iter[i])
    return result
