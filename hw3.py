import numpy as np
from fractions import Fraction as f
import random
import matplotlib.pyplot as plt
import math

# This will plot the amplitude of the function
def do_plot(measured_array):
	plt.plot(measured_array)
	plt.title('Amplitude')
	plt.xlabel('')
	plt.ylabel('Measurement')
	plt.show()

# Get random x for GCD(x, N) = 1
def get_x(Z):
	y = random.randint(2, Z-1)
	while math.gcd(y,Z) != 1:
		y = random.randint(2, Z-1)
	return y

# Get list of convergents
def get_convergents(x, y):
	z = get_frac(x,y)
	K = []
	l = len(z)
	while l != 0:
		K = K + [do_frac(z, l)]
		l = l - 1
	return K

# Get a list of values for the fraction
def get_frac(x, y, Z=[]):
	q = y//x
	Z = Z + [q]
	if y-q * x != 1 and y-q * x != 0:
		return get_frac(y-q*x, x, Z)
	else:
		Z = Z + [x]
		return Z

# Get fraction based on set Y
def do_frac(Y, n):
	Y = Y[0:n]
	if len(Y) == 1:
		return f(1, Y[0])
	else:
		return f(1, Y[0] + do_frac(Y[1:],n))

# Get measurement from probability
def do_measure(prob):
	r = random.random()
	for i in range(len(prob)):
		r = r - prob[i]
		if r  <= 0:
			return i
	return

# Fournier
def do_fourier(states):    
	N = len(states)
	if N != 1:
		W = 1
		p = (2 * math.pi) / N
		w = complex(math.cos(p), math.sin(p))
		a = states[0::2]
		b = states[1::2]
		y = do_fourier(a)
		x = do_fourier(b)
		Y = np.empty((N,1), dtype=complex)
		for j in range(0, N//2):
			Y[j] = y[j] + W * x[j]
			Y[j + N//2] = y[j] - W * x[j]
			W = W * w
	else:
		return states
	return Y

# Compute probability of pdf
def get_prob(dftvals, t2):
	probs = np.empty((t2,1))
	total_prob = 0
	for i in range(0, t2):
		probs[i] = math.pow(abs(dftvals[i]), 2)
		total_prob = total_prob + probs[i]
	return probs/total_prob

# Quantum steps
def do_quantum(x, N, t2):
	x_list = list()
	temp = 1
	x_list.append(temp)
	while True:
		temp = (temp * x) % N
		if temp == 1:
			break
		x_list.append(temp)
	measure=random.randint(0, len(x_list) - 1)
	collapse = range(measure, t2, len(x_list))
	result = np.zeros((t2,1))
	for i in collapse:
		result[i] = 1
	return result

# The main function used to run Peter Shor's algorithm.
# This will call the other functions in the proper order.
def do_shors(N):
	# Save array for the plotting stage
	measured_array = list()

	# Choose n and t
	n = math.ceil(math.log(N, 2))
	t = math.ceil(2 * math.log(N, 2))

	t2 = 2**t

	# Record number of attempts
	attempts = 0
	print("\nQBits:", n+t, "\n")
	done = False

	while not done:
		attempts = attempts + 1
		x = get_x(N)
		states = do_quantum(x, N, t2)
		temp_fourier = do_fourier(states)
		p = get_prob(temp_fourier, t2)
		measured = do_measure(p)

		while measured == 0:
			measured = do_measure(p)
		
		print("Measured:", measured)
		measured_array.append(measured)
		fracs = get_convergents(measured, t2)
		
		# Start r at 0
		r = 0
		
		for i in fracs:
			if i.denominator < N:
				r = i.denominator
				break
		print()
		
		if r % 2 == 1 and 2 * r < N:
			r = 2 * r

		factor =- 1
		if (math.pow(x,r)) % N != N - 1:
			if r % 2 == 0:
				a = math.gcd(x**(r//2) + 1, N)
				b = math.gcd(x**(r//2) + n - 1, N)
				factor = max(a, b)		
			if factor == 1 or factor == N:
				print("Got", factor, "rerunning...")			
			elif factor != -1:
				factor2 = N // factor
				do_test(factor, factor2, N, r, attempts, measured_array)
				done = True

# A function used to test the results and print them, then call the plot function		
def do_test(factor, factor2, N, r, attempts, measured_array):
	if (factor * factor2 == N):
		print ('-'*15)
		print ('Results')
		print ('-'*15)
		print ('Attempts:', attempts)
		print ('r:', r)
		print ('N:', N)
		print ('Factor:', factor)
		print ('Factor Two:', factor2)
		print ('Test passed!')
		do_plot(measured_array)
	else:
		print('Test failed.')
	print ('-'*15)

# Driver function to just run the shors function on execution
if __name__ == "__main__":
	do_shors(15)
	do_shors(143)