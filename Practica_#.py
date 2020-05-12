"""Redes Neuronales: Practica 3
   Alumno: Lic. García Fernández, Tomás Eugenio
   Maestria en Cs. Físicas
   Emails: tomas.garcia.fisica@gmail.com
           tomas.garcia.fisica@hotmail.com
"""
import numpy as np
from matplotlib import pyplot as plt

"""Funciones"""

def Tasa_disparo(sopike,num,num2):
    num=int(num)
    bins=int(10000/num)
    Rate_Spike=[]
    if sopike.ndim!=1:
        Suma=np.sum(sopike,axis=0)
        for i in range(num):
            Rate_Spike.append(np.sum(Suma[i*bins:bins+i*bins])/128)
    else:
        Suma=sopike
        for i in range(num):
            Rate_Spike.append(np.sum(Suma[i*bins:bins+i*bins]))
    plt.plot(range(num-1),Rate_Spike[1:])
    #plt.hist(Rate_Spike,bins=num2)   
    return Rate_Spike

def Factor_Fanon(spik):    
    n_prom=np.average(np.sum(spik,axis=1))
    var_n=np.average(np.sum(spike,axis=1)*np.sum(spike,axis=1))-n_prom*n_prom
    Fanon=var_n/n_prom
    print("El factor de Fanon es :",Fanon)

def Coeficiente_variabilidad(inter):
    tau=np.average(inter)
    tau2=np.average(inter*inter)-tau*tau
    CV=np.sqrt(tau2)/tau
    print("El coeficiente de variabilidad es :",CV)


def InterspikeIntervalo(spikes):
    """Funcion para crear una lista para graficar 
    los interspikes interval"""
    interspike_interval=[]
    for i in range(128):
        j=spikes[i][:].argmax()
        k=-1
        while True:
            if (spikes[i][j] == 1 and spikes[i][j+1:].max() == 1):
                maximo=spikes[i][j+1:].argmax()
                interspike_interval.append(maximo+1)
                j+=maximo+1
               
            if j==k:
                break
            k=j
    return interspike_interval

def Histograma_Pn(spikess):
    P__n=[]
    spike_flat=spikess.flatten()
    for i in range(int(spike_flat.shape[0]/1000)):
        P__n.append(np.sum(spike_flat[i*1000:(i+1)*1000]))    
    return P__n


"""Lectura de datos"""
spike=np.loadtxt("/home/tomas_vill/Escritorio/Redes_Neuro/Practica_3/Redes_/spike.dat")
stimulus=np.loadtxt("/home/tomas_vill/Escritorio/Redes_Neuro/Practica_3/Redes_/stimulus.dat")

""" Ejercicio a Armando el histograma de Interspike_interval bajo denominacion
Interspike_interval"""

Intervalo_Interspikes=InterspikeIntervalo(spike)

"""Coeficiente de Variabilidad"""

Coeficiente_variabilidad(np.array(Intervalo_Interspikes))

""" Ejercicio 2 Armando el histograma de P[n] bajo denominacion P_n"""

P_n=Histograma_Pn(spike)
# =============================================================================
# # Si quiero graficar ahora el P_n_ despues borrar
# =============================================================================
plt.hist(P_n,15)

"""Factor de Fanon"""
Factor_Fanon(spike)

"""Ejercicio 3 Armando el histograma de r[t] bajo denominacion r_t"""
Histograma=np.sum(spike,axis=0)/128

# =============================================================================
# Recontruccion de r(t) por método de ventada corrediza 
# =============================================================================
r_t=[]
num1=500
for i in range(10000-num1):
    r_t.append(np.average(Histograma[i:i+num1]))
plt.plot(range(10000-num1),r_t)

"""Graficasmos los datos obtenidos"""

fig,(Fig1,Fig2,Fig3)=plt.subplots(3,1)
Fig1.hist(Intervalo_Interspikes,25)
Fig2.hist(P_n,15)

plt.figure()

plt.subplot(121)
plt.hist(Intervalo_Interspikes,15)
plt.title("Interspike Intervarl")

plt.subplot(122)
plt.hist(P_n,15)
plt.title("P[n]")
plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,wspace=0.35)


# plt.savefig("Multi",format='pdf')
plt.show()
