import json
import matplotlib.pyplot as plt
from numpy import linspace
from scipy.fftpack import fft
import numpy as np

FILE_NAME = "mediciones/rc_10ciclos.json"

with open (FILE_NAME, "r") as file:
	medicion2 = json.load(file)

tiempo1 = medicion2["tiempo1"]
tiempo2 = medicion2["tiempo2"]
tension1 = medicion2["tension1"]
tension2 = medicion2["tension2"]




def fun_rc():
	delta_t = tiempo1[1] - tiempo1[0]
	fs = 1/delta_t

	resolucion_espectral = fs / len(tiempo1)

	palito = 1000 / resolucion_espectral

	print (palito)
	print(len(tiempo1))

	f = linspace(0, fs/2, len(tension1)//2, endpoint=False)

	#plt.plot(tiempo1,tension1,tiempo2,tension2)
	fft_var_1 = np.abs(fft(tension1))
	fft_phase_1 = np.angle(fft(tension1))

	plt.stem(f, fft_var_1[0:len(f)])
	plt.figure()
	plt.stem(f, fft_phase_1[0:len(f)])
	idx_1 = np.argmax(fft_var_1)
	print (f"hola {idx_1}")
	print(fft_phase_1[idx_1])

	fft_var_2 = np.abs(fft(tension2))
	fft_phase_2 = np.angle(fft(tension2))

	plt.stem(f, fft_var_2[0:len(f)])
	plt.figure()
	plt.stem(f, fft_phase_2[0:len(f)])
	idx_2 = np.argmax(fft_var_2)
	print (f"hola {idx_2}")
	print(fft_phase_2[idx_2])

	z_mod = fft_var_1[idx_1]/fft_var_2[idx_2]*1e3 #El canal 2 se midió con una resistencia de 1k.
	z_phase = fft_phase_1[idx_1] - fft_phase_2[idx_2]

	print(f"Módulo de la impedancia: {z_mod}")
	print(f"Ángulo de la impedancia: {np.rad2deg(z_phase)}")

	plt.show()

