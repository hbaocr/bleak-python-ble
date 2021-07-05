import analyse_util #import fft_analyse,butter_highpass,butter_lowpass,iir_notch,filter_data
import numpy as np
import time
import math
filename =  'ppg.csv'
filename =  'test.csv'
fs = 100
ppg = np.loadtxt(filename)

print(np.size(ppg))
tmp = time.time_ns()
# turn debug = true to see the graph. To run, this paras is False
hr,rr=analyse_util.ppg2rr(ppg,fs,debug=True)
print(">>> the process take: %d ms "%((time.time_ns()-tmp)/1000000))

print("rr= %d bpm"%(math.floor(rr)))
print("hr= %d bpm"%(math.floor(hr)))




