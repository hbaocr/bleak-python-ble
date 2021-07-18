import analyse_util #import fft_analyse,butter_highpass,butter_lowpass,iir_notch,filter_data
import numpy as np
import time
import math
filename =  'ppg.csv' #100Hz file
filename =  'ppg_25Hz.csv'
filename = "ppg_berrymed_100Hz.csv"
fs = 100
ppg = np.loadtxt(filename)[0:4000]

'''
F_target=100
ppg = analyse_util.resample(ppg,fs,F_target)
fs =F_target
'''
print("process on data size %d"%(np.size(ppg)))
tmp = time.time_ns()
# turn debug = true to see the graph. To run, this paras is False
hr,rr=analyse_util.ppg2rr(ppg,fs,debug=True)
print(">>> the process take: %d ms "%((time.time_ns()-tmp)/1000000))

print("rr= %d bpm"%(math.floor(rr)))
print("hr= %d bpm"%(math.floor(hr)))




