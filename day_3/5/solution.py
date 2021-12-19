import numpy as np

def bit_string_to_decimal(bit_string):
    num = 0
    nbits = len(bit_string)
    for i in range(nbits):
        power = nbits - i - 1
        num += (2**power) * int(bit_string[i])
    return num

def main():
    data = np.loadtxt("input", dtype=str)
    nbits = len(data[0])
    gamma_str = ""
    epsilon_str = ""
    for i in range(nbits):
        col = [d[i] for d in data]
        col = np.array(col).astype(int)
        num_zero = (col == 0).sum()
        num_one = (col == 1).sum()
        if num_zero > num_one:
            gamma_str += "0"
            epsilon_str += "1"
        else:
            gamma_str += "1"
            epsilon_str += "0"
    print("binary string:", gamma_str, epsilon_str)
    gamma = bit_string_to_decimal(gamma_str)
    epsilon = bit_string_to_decimal(epsilon_str)
    print("decimal:", gamma, epsilon)
    print("power:", gamma * epsilon)

if __name__ == "__main__":
    main()
