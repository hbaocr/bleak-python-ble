import analyse_util #import fft_analyse,butter_highpass,butter_lowpass,iir_notch,filter_data
import numpy as np
import time

from scipy.fft import fft, fftfreq
from scipy.signal import butter, lfilter, freqz,iirnotch
from csaps import csaps
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d

import matplotlib.pyplot as plt
import math

filename = "ppg_25hz_0rr.csv"
fs = 25
ppg = np.loadtxt(filename)

data_size =ppg.size
print(f"record time {data_size*1/fs/60} min")
window = 8*fs # 8 sec
step= 4*fs # 4sec
idx =0
x_sqi= np.array([])
y_sqi= np.array([])


while (idx <( data_size-window)):
    chunk = ppg[idx:(idx+window)]
    idx = idx + step
    hr,rr=analyse_util.ppg2rr(chunk,fs,debug=False)
    sqi=analyse_util.compute_ppg_SQI(chunk,hr,fs)
    x_sqi=np.append(x_sqi,[idx+window])
    y_sqi=np.append(y_sqi,[sqi])




   

plt.plot(ppg,'y',label="ppg")
plt.plot(x_sqi,y_sqi,'r',label="ppg")

plt.show()

'''










bad_start =[2000,2100,2200,2300,2400,2600,2700,3000,3100,3200,3300,3400,3500]

# good _ start : 1200 --> 2000 good
idx = 1200#bad_start[2]
chunk = ppg[idx:(idx+1*window)]



ppg = chunk
dppg = np.diff(ppg)

hr,rr=analyse_util.ppg2rr(ppg,fs,debug=False)
print(idx,hr,rr)

sigma = fs*60/hr/20
dppg_gauss = gaussian_filter1d(dppg,sigma)

dppg_gauss = threshold(dppg_gauss,0)

peaks, _=find_peaks(dppg_gauss,height=0)

print(peaks)
pulse_width = np.diff(peaks)
std = np.std(pulse_width)
avg = np.mean(pulse_width)
print(std,avg)



plt.subplot(3,1,1)

plt.plot(ppg,'y',label="ppg")
plt.plot(dppg_gauss,'g',label="dppg")
plt.plot(peaks,dppg_gauss[peaks],'xg',label="hist")
plt.plot(peaks,ppg[peaks],'*g',label="hist")

plt.subplot(3,1,2)
plt.plot(pulse_width,'*g',label="pw")


plt.subplot(3,1,3)
xf,yf=analyse_util.fft_analyse(ppg,fs)
smoothing_freq=analyse_util.smoothing_signal(xf, yf)
plt.plot(xf,yf,'y',label="Raw PSD")
plt.plot(xf,smoothing_freq,'r',label="Filtered PSD")
    




#hr,rr=analyse_util.ppg2rr(chunk,fs,debug=True)
plt.grid(True)
plt.legend(loc="upper right") # display the signal label on upper right
plt.show()











'''
