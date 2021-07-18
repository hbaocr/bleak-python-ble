from numpy.core.fromnumeric import compress
import analyse_util as util
import numpy as np

data_f = "./nir.txt"
#data_f = "./100hz_mylednir.txt"
data1 = np.loadtxt(data_f)[0:1000]
fs = 100
b1,a1 = util.butter_highpass(0.1,fs)
data = util.filter_data(data1,b1,a1)



#data = data-data_offset



#b1,a1 = util.butter_lowpass(10,fs)
#data = util.filter_data(data,b1,a1)


# remove   signal greater than  thresh_hold in F
def fun(e):
    thresh_hold =100
    if(e>thresh_hold):
        e=thresh_hold
    return e

compress_signal = np.vectorize(fun)



util.plt.subplot(2,1,1)
util.plt.plot(data1)
util.plt.grid()

util.plt.subplot(2,1,2)
xf,yf = util.fft_analyse(data,fs)

yf= compress_signal(yf)
util.plt.plot(xf,yf)

#util.plt.plot(data)
util.plt.grid()
util.plt.show()



'''
data_f ="./PPG100Hz_RED_GREEN_NIR.txt"
data = np.loadtxt(data_f)
print(len(data))
fs = 100
red =np.array([])
green =np.array([])
nir =np.array([])

for i in range(len(data)-100):
    red = np.append(red,data[i][0])
    green = np.append(green,data[i][1])
    nir = np.append(nir,data[i][2])

b1,a1 = util.butter_highpass(1,fs)
green = util.filter_data(green,b1,a1)

xf,yf = util.fft_analyse(green,fs)
util.plt.plot(xf,yf)


'''

#util.plt.plot(green)
#util.plt.plot(green)
#util.plt.plot(nir)
util.plt.show()
'''
b1,a1 = util.butter_highpass(0.1,fs)
red = util.filter_data(green,b1,a1)
xf,yf = util.fft_analyse(red,fs)
util.plt.plot(xf,yf)
util.plt.show()
'''





