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
def Tiggered_time(num):
    tigger_av=lambda size_wind,vuelta: [sum(stimulus[i-size_wind:i,1]/0.1*size_wind) for i in range(len(spike[0])) if spike[vuelta][i]==1]
    # Determino s(ti-tau) para un tau fijo y un determinado trial
    # La funcion devuelve una lista con los n s(ti-tau)
    prom_tigg=lambda  size:[np.mean(tigger_av(size,i)) for i in range(128) ]
    # Determino C(tau): el promedio de los s(ti-tau)
    # La funcion devuelve una lista con los 128 C(tau) de todos los trial para un mismo tau
    prom_tigg_trial=lambda num: [np.mean(prom_tigg(i)) for i in range(num)]
    #Determino C en funcion de tau 
    # La funcion devuelve una lista con C en funcion de tau 
    graf=lambda num: plt.plot(range(num),prom_tigg_trial(num) )
    #Grafica
    return prom_tigg_trial(num)

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

# =============================================================================
# Determinar el Spike-Tiggeered Average
# =============================================================================
Tigger=Tiggered_time(15)
"""Graficasmos los datos obtenidos"""

fig,(Fig1,Fig2,Fig3,Fig4)=plt.subplots(4,1,figsize=(20,35))
Fig1.hist(Intervalo_Interspikes,25,label="InterSpike_Interval")
Fig1.legend()
Fig1.autoscale()
Fig2.hist(P_n,15,label="Histograma P(n)")
Fig2.legend()
Fig2.autoscale()
Fig3.plot([i*0.1 for i in range(10000-num1)],r_t,label="Histograma r(t)")
Fig3.legend()
Fig3.autoscale()
Fig4.plot([i*0.1 for i in range(len(Tigger))],Tigger,label="Spike-Tiggered Average")
Fig4.legend()
Fig4.autoscale()



