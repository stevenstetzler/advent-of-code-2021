import numpy as np
import os
import sys

def main():
	data = np.loadtxt("input", dtype=int)
	window_size = 3
	num_increased = 0
	for i in range(0, data.shape[0] - window_size):
		window_1 = slice(i, i + window_size)
		window_2 = slice(i + 1, i + 1 + window_size)
		increased = data[window_2].sum() > data[window_1].sum()
		if increased:
			num_increased += 1
	print(num_increased)

if __name__ == "__main__":
	main()

