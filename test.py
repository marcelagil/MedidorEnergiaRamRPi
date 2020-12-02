#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError
from datetime import datetime
import time
import os
from subprocess import Popen, PIPE
from signal import SIGTERM

MAX_EXPECTED_AMPS = 2
SHUNT_OHMS = 0.1
nombreArchivo  = "/home/pi/Desktop/MedidorEnergiaRamRPi/resultados"
nombreProceso="node"
DELAY=0.2
#DELAY=0.002
NUM_MUESTRAS=int(10.5*60/DELAY)

def calculoMemoria():
    """
    Calcula  la memoria usara
    """
    with open('/proc/meminfo', 'r') as mem:
        ret = {}
        tmp = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) == 'MemTotal:':
                ret['total'] = int(sline[1])
            elif str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                tmp += int(sline[1])
                ret['libre'] = tmp
                ret['usada'] = int(ret['total']) - int(ret['libre'])
    return ret

def mideEnergiaRAM():
    fechaIncial= time.strftime("%d-%m_")
    horaInicial=time.strftime("%H_%M_%S")
    archivoResultados=nombreArchivo+fechaIncial+horaInicial+".csv"
    print(archivoResultados)
    a = open (archivoResultados,'a')
    a.write("N° medida;Fecha;Voltaje Shunt;Voltaje Bus;Voltaje total;Corriente;Potencia;Memoria Libre; Memoria Usada;Memoria Total;Proceso Node\n")
    try:
        for i in range(NUM_MUESTRAS):
            fechaHora =  datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            voltajeShunt="h"
            voltajeBus="h"
            voltajeTotal="h"
            corriente="h"
            potencia="h"
            contador=str(i+1)
            memoria=calculoMemoria()
            memoriaLibre=str(memoria['libre'])
            memoriaUsada=str(memoria['usada'])
            memoriaTotal=str(memoria['total'])
            activo=detectaProcesoActivo(nombreProceso)
            textoArchivo= contador+';'+fechaHora+';'+voltajeShunt+';'+voltajeBus+';'+voltajeTotal+';'+corriente+';'+potencia+';'+memoriaLibre+';'+memoriaUsada+';'+memoriaTotal+';'+activo+'\n'
            a.write(textoArchivo)
            print(memoria)
            print(textoArchivo)
            time.sleep(DELAY)
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print(e)
    a.close()

def detectaProcesoActivo (nombre):
    ps= Popen(["ps", "-e"], stdout=PIPE)
    grep = Popen(["grep", nombre], stdin=ps.stdout, stdout=PIPE)
    ps.stdout.close()
    data = grep.stdout.read().decode()
    if data:
        print("Proceso activo con nombre: "+ nombre)
        return "Activo"
    else:
        print("El proceso no està activo")
        return "No Activo"

if __name__ == "__main__":
    mideEnergiaRAM()

## fin
