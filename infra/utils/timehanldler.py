from datetime import datetime


def get_partial_timestamp(number=10):
    timestamp = datetime.now().timestamp()
    int_float = str(timestamp).split('.')
    int_number_str = int_float[0]
    float_number_str = int_float[1]
    if number <= 10:
        start = 10 - number - 1
        return int_number_str[start:]
    sub_num = number - 10
    sub_num = 6 if sub_num > 6 else sub_num
    return int_number_str + float_number_str[:sub_num]


if __name__ == '__main__':
    print(get_partial_timestamp(4))