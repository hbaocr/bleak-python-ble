# from common import resample_data
import math
import numpy as np
from scipy.fft import fft, fftfreq
from scipy.signal import butter, lfilter, iirnotch, find_peaks
from scipy.ndimage import gaussian_filter1d

from csaps import csaps
import matplotlib.pyplot as plt
# analyse original
def resample(signal, f_signal, f_target=125):
    resample_rate = f_signal / f_target
    return np.interp(np.arange(0, len(signal), resample_rate), np.arange(0, len(signal)), signal)


def fft_analyse(dt, fs):
    N = np.size(dt)
    T = 1 / fs
    xf = fftfreq(N, T)[:N // 2]
    yf = fft(dt)
    return (xf, 2.0 / N * np.abs(yf[0:N // 2]))


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(N=order, Wn=normal_cutoff, btype='lowpass')
    return b, a


def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(N=order, Wn=normal_cutoff, btype='highpass')
    return b, a


def iir_notch(freq_notch, fs, order=5, quality_factor=30):
    # nyq = 0.5 * fs
    # notch = freq_notch / nyq
    # Quality = 80  # w0/bw
    b, a = iirnotch(w0=freq_notch, Q=quality_factor, fs=fs)
    return b, a


def filter_data(signal, b, a):
    y = lfilter(b, a, signal)
    return y


def smoothing_signal(xf_, yf_, smooth_=0.99):
    nyf = csaps(xf_, yf_, xf_, smooth=0.99)
    return nyf

# 0.1Hz < RR < 0.6hz


def find_HR_RR(xf_, yf_, rr_max=0.6, rr_min=0.1):
    hr_idx = np.argmax(yf_)
    hr = xf_[hr_idx] 
    # nyf = yf_ #yf_[:(hr_idx)] # get idx from 0...HR peak to find RR
    nyf = yf_[:(hr_idx)]
    peaks, _ = find_peaks(nyf, height=0)
    rr = 0
    rr_index = 0
    for rr_idx in peaks:
        tmp = xf_[rr_idx]
        if(tmp < rr_max and tmp > rr and tmp > rr_min):
            rr = tmp
            rr_index = rr_idx

    return hr*60, rr * 60, hr_idx, rr_index


def ppg2rr(ppg, fs, debug = False):
    f_dc_remove = 0.15
    b, a = butter_highpass(f_dc_remove, fs)
    ppg_f = filter_data(ppg, b, a)
    # fft
    xf, yf = fft_analyse(ppg_f, fs)
    smoothing_freq = smoothing_signal(xf, yf)
    hr, rr, hr_idx, rr_idx = find_HR_RR(xf, smoothing_freq)
    if debug:
        print("rr= %d bpm" % (math.floor(rr)))
        print("hr= %d bpm" % (math.floor(hr)))
        # peaks, _ = find_peaks(smoothing_freq, height=0)
        # peaks = np.array([rr_idx, hr_idx])

        plt.subplot(2, 1, 1)
        plt.plot(ppg, label="PPG")
        plt.grid()
        plt.legend(loc="upper right")  # display the signal label on upper right
        plt.title('PPG')

        plt.subplot(2, 1, 2)
        # plt.title('Analyse')
        plt.plot(xf, yf, 'y', label="Raw PSD")
        plt.plot(xf, smoothing_freq, 'r', label="Filtered PSD")
        # plt.plot(xf[peaks],smoothing_freq[peaks],'x')
        plt.plot(xf[rr_idx], smoothing_freq[rr_idx], '*', label=f"RR:{rr//1} bpm")
        # plt.text(xf[rr_idx],smoothing_freq[rr_idx],f"RR:{rr//1} bpm")

        plt.plot(xf[hr_idx], smoothing_freq[hr_idx], 'o', label=f"HR:{hr//1} bpm")
        # plt.text(xf[hr_idx],smoothing_freq[hr_idx],f"HR:{hr//1} bpm")
        plt.grid(True)
        plt.legend(loc="upper right")  # display the signal label on upper right
        plt.show()
    return hr, rr

def threshold(signal,thr_lev=0,thr_val=0):
    thr_fn = lambda t: thr_val if t < thr_lev else t
    fn = np.vectorize(thr_fn)
    return fn(signal)

def compute_ppg_SQI(ppg_signal,fft_hr_bpm,fs,std_tolerance=1.2):
    # segment all the HR period session by finding the maximum peak of diff(ppg_signal).
    # The position idx of maximum rising peaks of dppg is used to determine the start position of each HR segment
    # And the distance between each start point is considered as the computed HR, this value will
    # compare with the HR retrive by FFT, if they are not so different ==> this good signal 
    fft_hr_pulse_width = 60*fs/fft_hr_bpm
    dppg =np.diff(ppg_signal)
    sigma = fft_hr_pulse_width/20
    dppg_gauss = gaussian_filter1d(dppg,sigma)

    # Get all the rising peaks of dppg ( rising Systolic peaks and potential rising diatolic peak)
    # rising Systolic peaks (dPPG systolic phase) >>  potential rising diatolic peak(dPPG diatolic phase)
    all_rising_slopes = threshold(dppg_gauss,0) # only get rising slopes 
    all_rising_peaks_idx, _=find_peaks(all_rising_slopes,height=0)
    all_rising_peaks=all_rising_slopes[all_rising_peaks_idx]
    
    #  the  number of HR peaks  <  1/2 Estimated peaks = 1/2  * (signal_total_len /HR_PULES_WIDTH ) 
    if(all_rising_peaks.size < dppg_gauss.size/(2*fft_hr_pulse_width)):
        return 0

    #only keep rising Systolic peaks (dPPG systolic phase) 
    # ==> using for determine start possion of each HR segment
    mean = np.median(all_rising_peaks)
    std = np.std(all_rising_peaks)
    thr = mean - std_tolerance*std
    rising_hr_slopes = threshold(dppg_gauss,thr) # only get rising slopes
    rising_hr_peaks_idx, _=find_peaks(rising_hr_slopes,height=0)

    # distance between start possion of each HR segment is HR pulse width
    ppg_pulse_width = np.diff(rising_hr_peaks_idx)
   
    #  the  number of HR peaks  <  1/2 Estimated peaks = 1/2  * (signal_total_len /HR_PULES_WIDTH ) 
    if(ppg_pulse_width.size < dppg_gauss.size/(2*fft_hr_pulse_width)):
        return 0

    
    dist_arr = ppg_pulse_width-fft_hr_pulse_width
    rms_dist  = np.sqrt(np.mean(np.square(dist_arr)))
    rms_dist_norm_fs = rms_dist/fs
    # sqi 100 is best signal , 0 : bad signal
    sqi= math.floor(2*100 / (1 + math.exp(rms_dist_norm_fs))) 
    return sqi





