MAX_EXPECTED_AMPS = 0.2

nombreArchivo  = "resultados"
DELAY=0.2
#DELAY=0.002
NUM_MUESTRAS=450000

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
    ina = INA219(SHUNT_OHMS)
    ina.configure(ina.RANGE_16V)
    fechaIncial= time.strftime("%d-%m_")
    horaInicial=time.strftime("%H_%M_%S")
    archivoResultados=nombreArchivo+fechaIncial+horaInicial+"csv"
    print("Bus Voltage: %.3f V" % ina.voltage())
    a = open (archivoResultados,'a')
    a.write("N° medida,Fecha,Voltaje Shunt,Voltaje Bus,Voltaje total,Corriente,Potencia,Memoria Libre, Memoria Usada,Memoria Total\n")
    try:
        for i in range(NUM_MUESTRAS):
            fechaHora =  time.strftime("%c")
            print("Bus Current: %.3f mA" % ina.current())
            print("Power: %.3f mW" % ina.power())
            print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
            print("Voltaje : %.3f V " % ina.voltage())
            print("Voltaje : %.3f V " % ina.supply_voltage())
            voltajeShunt=ina.shunt_voltage()
            voltajeBus=str(ina.voltage())
            voltajeTotal=ina.supply_voltage())
            corriente=str(ina.current())
            potencia=str(ina.power())
            contador=str(i+1)
            memoria=calculoMemoria()
            memoriaLibre=str(memoria.libre)
            memoriaUsada=str(memoria.usada)
            memoriaTotal=str(memoria.total)
            textoArchivo= contador+','+fecha+','+voltajeShunt+','+voltajeBus+','+voltajeTotal+','+corriente+','+potencia+','+memoriaLibre+','+memoriaUsada+','+memoriaTotal\n'
            a.write(textoArchivo)
            time.sleep(DELAY)
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print(e)
    a.close()

if __name__ == "__main__":
    mideEnergiaRAM()

## fin