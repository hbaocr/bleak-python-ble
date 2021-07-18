import numpy as np
from scipy.fft import fft, fftfreq
from scipy.signal import butter, lfilter, iirnotch
from csaps import csaps
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import math
import analyse_util as ppg2rr



def rms(signal):
   sq=np.square(signal) #x^2
   pwr = np.mean(sq)
   return np.sqrt(pwr)

def standard_deviation(signal):
    return np.std(signal) 

def max_abs(signal):
    return np.mean(signal)

def mean(signal):
   
    return np.max(np.abs(signal))


#rand_int3 = np.random.randint(50,75,(2,2), dtype='int32')
#print("Third array", rand_int3)
fs = 25
epsilon = 10
len = 16*fs
mean  = 100
std = 0
ppg = np.random.randint(mean-std,mean+std+1,(1,len))[0]
#dx=1 #t2-t1
#dydx = np.gradient(ppg, dx)

hr, rr = ppg2rr.ppg2rr(ppg, fs, True)
print(hr, rr)


