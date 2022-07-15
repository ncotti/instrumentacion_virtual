# Traemos la libreria VISA
import pyvisa as visa
import numpy as np
# Traemos matplotlib para poder graficar
import matplotlib.pyplot as plt
# Agreamos el path de las librerias
import sys
sys.path.insert(0, 'InstVirtualLib')
import platform
# Traemos todos los osciloscopios
from InstVirtualLib.osciloscopios import GW_Instek
from InstVirtualLib.osciloscopios import rigol
from InstVirtualLib.osciloscopios import Tektronix_DSO_DPO_MSO_TDS
# Traemos el operador
import operador
import json

# Definimos una funcion para poder ejecutar un mensaje de error
def excepthook(type, value, traceback):
    print(value)

sys.excepthook = excepthook



# Seteamos el tipo de osciloscio a utilizar
OSCILOSCOPIOS = 0	# 0: GW_Instek
			# 1: rigol
			# 2: Tektronix_DSO_DPO_MSO_TDS

USE_DEVICE = 0

# Abrimos el instrumento
platforma = platform.platform()
print(platforma)
if 'pyvisa' in sys.modules:
	rm=visa.ResourceManager('@py')
	print('pyvisa')
elif 'visa' in sys.modules:
	rm=visa.ResourceManager('@ni')
	print('visa')
else:
	error()

instrument_handler=rm.open_resource(rm.list_resources()[USE_DEVICE])

if OSCILOSCOPIOS == 0:
	MiOsciloscopio = GW_Instek(instrument_handler)
elif OSCILOSCOPIOS == 1:
	MiOsciloscopio = rigol(instrument_handler)
elif OSCILOSCOPIOS == 2:
	MiOsciloscopio = Tektronix_DSO_DPO_MSO_TDS(instrument_handler)
else:
	raise ValueError('Tipo de osciloscopio fuera de lista.')


# Informamos el modelo del osciloscopio conectado
print("Esta conectado un %s"%MiOsciloscopio.INSTR_ID)


# Pedimos el trazo de cada canal, la salida es en ([seg.],[volt])
tiempo1,tension1=MiOsciloscopio.get_trace("1", VERBOSE=0)
tiempo2,tension2=MiOsciloscopio.get_trace("2", VERBOSE=0)

print (type(tiempo1))
# Ploteamos los canales
medicion = {
	"tiempo1":  np.ndarray.tolist(tiempo1),
	"tiempo2":  np.ndarray.tolist(tiempo2),
	"tension1": np.ndarray.tolist(tension1),
	"tension2": np.ndarray.tolist(tension2)
}

# with open ("data.json", "r") as file:
# 	medicion2 = json.load(file)

# tiempo1 = medicion2["tiempo1"]
# tiempo2 = medicion2["tiempo2"]
# tension1 = medicion2["tension1"]
# tension2 = medicion2["tension2"]

plt.plot(tiempo1,tension1,tiempo2,tension2)
plt.show()



with open ("data.json", "w") as file:
	json.dump(medicion, file)





# Generamos un operador y pedimos el valor RMS actual
operador_1 = operador.Operador(MiOsciloscopio,"Workbench_I")

val_RMS = operador_1.medir_Vrms(canal = 1, VERBOSE = True)

print('Vrms = %0.5f'%val_RMS)


MiOsciloscopio.close()
