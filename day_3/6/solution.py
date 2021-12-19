import numpy as np

def bit_string_to_decimal(bit_string):
    num = 0
    nbits = len(bit_string)
    for i in range(nbits):
        power = nbits - i - 1
        num += (2**power) * int(bit_string[i])
    return num

def keep_ones(s, position):
    return s[position] == "1"

def keep_zeros(s, position):
    return s[position] == "0"

def filter_co2(bit_string_list, position):
    column = [d[position] for d in bit_string_list]
    column = np.array(column)
    num_zero = (column == "0").sum()
    num_one = (column == "1").sum()
    if num_zero > num_one:
        return bit_string_list[np.where(column == "1")]
    else:
        return bit_string_list[np.where(column == "0")]

def filter_oxygen(bit_string_list, position):
    column = [d[position] for d in bit_string_list]
    column = np.array(column)
    num_zero = (column == "0").sum()
    num_one = (column == "1").sum()
    if num_zero > num_one:
        return bit_string_list[column == "0"]
    else:
        return bit_string_list[column == "1"]

def filter_for_value(data, bit_criteria):
    nbits = len(data[0])
    _data = np.copy(data)
    for i in range(nbits):
        _data = bit_criteria(_data, i)
        if len(_data) == 1:
            print("found value after position", i, _data)
            break
    if len(_data) != 1:
        print("more than 1 bit string left:", _data)
    value_str = _data[0]
    return value_str

def main():
    data = np.loadtxt("input", dtype=str)

    oxygen_str = filter_for_value(data, filter_oxygen)
    co2_str = filter_for_value(data, filter_co2)

    oxygen = bit_string_to_decimal(oxygen_str)
    co2 = bit_string_to_decimal(co2_str)

    print(oxygen, co2, oxygen*co2)

if __name__ == "__main__":
    main()
