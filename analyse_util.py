
#from common import resample_data
import numpy as np
from scipy.fft import fft, fftfreq
from scipy.signal import butter, lfilter, freqz,iirnotch
from csaps import csaps
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import math
######analyse original
def fft_analyse(dt,fs):
    N= np.size(dt)
    T = 1/fs
    xf = fftfreq(N, T)[:N//2]
    yf = fft(dt)
    return (xf,2.0/N * np.abs(yf[0:N//2]))

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a =butter(N=order,Wn=normal_cutoff,btype='lowpass')
    return b, a

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a =butter(N=order,Wn=normal_cutoff,btype='highpass')
    return b, a

def iir_notch(freq_notch, fs, order=5,quality_factor=30):
    nyq = 0.5 * fs
    notch = freq_notch / nyq
    Quality = 80#w0/bw
    b,a = iirnotch(w0=freq_notch,Q=quality_factor,fs=fs)
    return b, a


def filter_data(signal,b,a):
    y = lfilter(b, a, signal)
    return y

def smoothing_signal(xf_,yf_,smooth_=0.99):
    nyf = csaps(xf_, yf_, xf_, smooth=0.99)
    return nyf

# RR < 0.6hz
def find_HR_RR(xf_,yf_,rr_max=0.6):
        hr_idx = np.argmax(yf_)
        hr = xf_[hr_idx]*60
        nyf = yf_ #yf_[:(hr_idx)] # get idx from 0...HR peak to find RR
        peaks, _ = find_peaks(nyf, height=0)
        rr=0
        for rr_idx in peaks:
            tmp=xf_[rr_idx]
            if(tmp<rr_max and tmp>rr):
                rr = tmp
        return hr,rr*60

def ppg2rr(ppg,fs,debug = False):
    f_dc_remove = 0.15
    b,a = butter_highpass(f_dc_remove,fs)
    ppg_f = filter_data(ppg,b,a)
    # fft
    xf,yf=fft_analyse(ppg_f,fs)
    smoothing_freq=smoothing_signal(xf, yf)
    hr,rr=find_HR_RR(xf,smoothing_freq);
    if debug==True:
        print("rr= %d bpm"%(math.floor(rr)))
        print("hr= %d bpm"%(math.floor(hr)))
        peaks, _ = find_peaks(smoothing_freq, height=0)
        plt.plot(xf,yf,'y')
        plt.plot(xf,smoothing_freq,'r')
        plt.plot(xf[peaks],smoothing_freq[peaks],'x')
        plt.grid(True)
        plt.show()
    return hr,rr

