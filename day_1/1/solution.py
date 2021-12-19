import numpy as np
import os
import sys

def main():
	data = np.loadtxt("input", dtype=int)
	num_increased = 0
	for i in range(0, data.shape[0] - 1):
		increased = data[i + 1] > data[i]
		if increased:
			num_increased += 1
	print(num_increased)

if __name__ == "__main__":
	main()

