import numpy as np
from fractions import Fraction
import random
import math
import cmath

# Get random x for GCD(x, N) = 1
def get_x(Z):
	y = random.randint(2, Z-1)
	while math.gcd(y,Z) != 1:
		y = random.randint(2, Z-1)
	return y

def quantum(x, N, t2):
	xmodn = []
	xmodn.append(1)
	temp = 1
	while True:
		temp = (temp*x) % N
		if temp == 1:
			break
		xmodn.append(temp)
	measure=random.randint(0, len(xmodn) - 1)
	collapse = range(measure, t2, len(xmodn))
	result = np.zeros((t2,1))
	for i in collapse:
		result[i] = 1
	return result

"Measures a value from a normalized probability distribution"
def nonuniform_measure(prob):
	r = random.random()
	for i in range(len(prob)):
		r = r - prob[i]
		if r  <= 0:
			return i
	return

"CALCULATE CONTINUED FRACTIONS"
"Returns the list of all convergents of the fraction x/y"
def list_convergents(x,y):
	z = find_continued_fraction(x,y)
	K = []
	m = len(z)
	while m!= 0:
		K = K + [do_frac(z,m)]
		m = m - 1
	return K

"Returns the list of values in the continued fraction of x/y"
def find_continued_fraction(x,y,Z=[]):
	q=y//x
	Z = Z + [q]
	if y-q*x!=1 and y-q*x!=0:
		return find_continued_fraction(y-q*x,x,Z)
	else:
		Z+=[x]
		return Z

"Returns the fraction associated with a set Y of values in a continued fraction, using the first n values of Y or all values if n>len(Y)"
def do_frac(Y,n):
	Y=Y[0:n]
	if len(Y)==1:
		return Fraction(1,Y[0])
	else:
		return Fraction(1,Y[0]+do_frac(Y[1:],n))

# Fournier
def do_fourier(states):    
	N = len(states)
	if N == 1 :
		return states
	else :
		W = 1
		phi = (2 * math.pi ) / N
		Wn = complex(math.cos(phi), math.sin(phi))
		Aeven = states[0::2]
		Aodd = states[1::2]
		Yeven = do_fourier(Aeven)
		Yodd = do_fourier(Aodd)
		Y = np.empty((N,1),dtype=complex)
		for j in range(0, N//2):
			Y[j] = Yeven[j] + W * Yodd[j]
			Y[j + N//2] = Yeven[j] - W * Yodd[j]
			W = W * Wn
	return Y

# Compute probability of pdf
def allprobs(dftvals, t2):
	probs = np.empty((t2,1))
	total_prob = 0
	for i in range(0, t2):
		probs[i] = math.pow(abs(dftvals[i]), 2)
		total_prob = total_prob + probs[i]
	return probs/total_prob

# The main function used to run Peter Shor's algorithm.
# This will call the other functions in the proper order.
def Shor(N):
	n = math.ceil(math.log(N, 2))
	t = math.ceil(2*math.log(N, 2))
	t2 = 2**t
	attempts = 0
	print("\nQBits:", n+t, "\n")
	done = False

	while not done:
		attempts = attempts + 1
		print("Attempt:", attempts)
		x = get_x(N)
		print("x:", x)

		states = quantum(x, N, t2)
		temp_fourier = do_fourier(states)
		pdf = allprobs(temp_fourier, t2)
		measured = nonuniform_measure(pdf)

		while measured == 0:
			measured = nonuniform_measure(pdf)
		
		print("Measured:", measured)
		fracs = list_convergents(measured, t2)
		r = 0
		for f in fracs:
			if f.denominator < N:
				r = f.denominator
				break
		print()
		if r % 2 == 1 and 2 * r < N:
			r = 2 * r

		factor =- 1
		if (math.pow(x,r)) % N != N - 1:
			if r % 2 == 0:
				a = math.gcd(x**(r//2) + 1, N)
				b = math.gcd(x**(r//2) + n-1, N)
				factor = max(a, b)				
			if factor == 1 or factor == N:
				print("Got", factor, "rerunning...\n")			
			elif factor != -1:
				factor2 = N // factor
				do_test(factor, factor2, N, r)
				done = True
		
def do_test(factor, factor2, N, r):
	if (factor*factor2 == N):
		print ('-'*15)
		print ('Results')
		print ('-'*15)
		print ('r:', r)
		print ('N:', N)
		print ('Factor:', factor)
		print ('Factor Two:', factor2)
		print ('Test passed!')
	else:
		print('Test failed.')
	print ('-'*15)

if __name__ == "__main__":
	Shor(143)
