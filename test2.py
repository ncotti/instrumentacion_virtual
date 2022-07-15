import numpy as np
from matplotlib import pyplot as plt
from scipy import signal as sg

###############################################################################
#   Definición de funciones
###############################################################################
n = 1.2
t = np.linspace(0, 2*np.pi, 100, endpoint=False)
x = np.cos(n*t)

flattop = sg.windows.flattop(len(x))
hanning = sg.hann(len(x))
rectangular = np.ones(len(x))

hanning_f = abs(np.fft.fft(hanning,1024))
hanning_f =  hanning_f[0:len(x)//2] /len(x)*2
response = 20*np.log10(np.abs(np.fft.fftshift(hanning_f)))

rectangular_f = abs(np.fft.fft(rectangular,1024))
rectangular_f =  rectangular_f[0:len(x)//2] /len(x)*2


plt.figure(5)
# plt.subplot(111)
# plt.plot(t, hanning)
# plt.subplot(211)
plt.plot(response)

# plt.figure(2)
# plt.subplot(1)
# plt.plot(t, rectangular)





plt.figure(1)
plt.plot(t, x)

plt.figure(2)
#plt.stem(f)

# f = abs(np.fft.fft(rectangular, 1024))
# f = f[0:len(x)//2]
# f = f/len(x)*2
# f = 20*np.log10(np.abs(np.fft.fftshift(f)))

# plt.stem(f)

# f = abs(np.fft.fft(hanning, 1024))
# f = f[0:len(x)//2]
# f = f/len(x)*2
# f = 20*np.log10(np.abs(np.fft.fftshift(f)))

# plt.stem(f)

plt.show()
