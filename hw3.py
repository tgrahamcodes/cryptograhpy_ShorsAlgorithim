#/opt/homebrew/bin/python3
# Tom Graham
# Advanced Crypto
# Project 3
import math
import matplotlib.pyplot as p
import numpy as np

# Plot the amplitude of the different states
# of the Quantum Registers after each major step of Shor's
def plot():
	# TODO
	print ("Plotting")
	frequency = 100
	interval = 1/frequency
	start_time = 0
	end_time = 10
	time = np.arange(start_time, end_time, interval)

	amplitude_one = np.sin(2*np.pi*frequency*time)
	amplitude_two = np.sin(2*np.pi*frequency*time)

	figure, axis = p.subplots(4, 1)
	p.subplots_adjust(hspace=1)

	axis[0].set_title('Sine wave with a frequency of 4 Hz')
	axis[0].plot(time, amplitude_one)
	axis[0].set_xlabel('Time')
	axis[0].set_ylabel('Amplitude')

	axis[1].set_title('Sine wave with a frequency of 7 Hz')
	axis[1].plot(time, amplitude_two)
	axis[1].set_xlabel('Time')
	axis[1].set_ylabel('Amplitude')

	amplitude = amplitude_one + amplitude_two

	axis[2].set_title('Sine wave with multiple frequencies')
	axis[2].plot(time, amplitude)
	axis[2].set_xlabel('Time')
	axis[2].set_ylabel('Amplitude')

	fourierTransform = np.fft.fft(amplitude)/len(amplitude)           
	fourierTransform = fourierTransform[range(int(len(amplitude)/2))] 

	tpCount     = len(amplitude)
	values      = np.arange(int(tpCount/2))
	timePeriod  = tpCount/frequency
	frequencies = values/timePeriod

	axis[3].set_title('Fourier transform depicting the frequency components')
	axis[3].plot(frequencies, abs(fourierTransform))
	axis[3].set_xlabel('Frequency')
	axis[3].set_ylabel('Amplitude')

	p.show()

# Classical part which reduces the factorisation to a problem of finding the period of the function. This is done classically using a normal computer.
def shors_step_one():
	print("Shors step one function")
	# return period

# Quantum part which uses a quantum computer to find the period using the Quantum Fourier Transform.
def shors_step_two():
	print("Shors step two function")
	# return period

# Simulate the index finding algorithm in Shor’s quantum factorization algorithm 
if __name__ == "__main__":
	# random number such that A < N
	A = 6

	QBits = 6 
	# iterate 2^12 times
	# should see period, 2^6 = 64 / 8 = 8 times

	# Part one of HW
	n = 15

	# p * q = p is 3, q is 5
	period = 8

	# 143 = 11 * 13 = 10 * 12 = 120 bits = 2^7 (128)
	# 12 or 13 qbits
	
	# f(x) = a^(x mod n)
	# peroidic, discrete problem in finite set

	# Part two of HW
	n2 = 143
	
	gcd = math.gcd(n)
	# plot()

	# Computer the gcd of N
	# run quatum circuit using a Quantum Fourier Transform
	if (gcd != 1): 
	 	print ("Found factor of N", gcd)
	#	else:
	#		if (period % 2):
	#	 		return shors_step_one()