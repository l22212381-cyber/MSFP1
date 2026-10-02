"""
Práctica 1: Diseño de controladores

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Nayeli Bonilla Martinez
Número de control: 22212381
Correo institucional: l22212381@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot
# Respuesta del sistema en lazo abierto y en lazo cerrado
import numpy as np 
import math as m
import control as ctrl 
import matplotlib.pyplot as plt

#Datos generales de la simulacion 
x0, t0, tend, dt, w, h = 0, 0, 10, 1E-3,7, 3.5
N= round (tend/dt) +1 
t = np.linspace(t0,tend,N)
u1= np.ones(N)
u2=np.zeros(N); u2[round (1/dt):round(2/dt)]=1
u3= t/tend
u4= np.sin(m.pi/2*t)
u= np.column_stack((u1,u2,u3,u4))
signals=["step","impulse","ramp","sinusoidal"]

#componentes del circuito RLC
R,L,C=10E3, 220E-6, 470E-6
num= [C*L*R,C*R**2+L,R]
den=[3*C*L*R,5*C*R**2+L,2*R]
sys= ctrl.tf(num,den)
print(f"Funcion de transferencia: {sys}\n")

#Polos del sistema
L=np.roots(den)
print (f"Polos del sistema: L1= {L[0]:.3e}, L2={L[1]:.3e}\n")

#Componentes del controlador 
kI = 473.9312622100245
Cr= 1E-6
Re = 1/(Cr*kI)
numPID= [1]
denPID= [Re*Cr,0]
PID = ctrl.tf(numPID, denPID)

print (f"Capacitancia Cr: {Cr} Faradios \n")
print (f"Resistencia Re: {Re} ohms \n")
print (f"Funcion de transferencia del controlador:{PID} \n")

#Sistema de control en lazo cerrado
sysPID= ctrl.feedback(ctrl.series(PID,sys))
print(f"Funcion de transferencia en lazo cerrado: {sysPID}\n")

clr1 = np.array([139, 30, 45])/225
clr2 = np.array([51, 104, 160])/225
clr3 = np.array([18, 84, 79])/225

#Funciones del sistema en lazo abierto y lazo cerrado
def openloop(t, sys, u):
    _, _PAu = ctrl.forced_response(sys, t, u, X0=x0)
    return _PAu

def closedloop(t, sysPID, u):
    _, _PIDu = ctrl.forced_response(sysPID, t, u, X0=x0)
    return _PIDu
#Respuestas: simulaciones numericas 
for i in range(0,4):
    PAu = openloop(t,sys,u[:,i])
    PIDu = closedloop(t,sysPID,u[:,i])
    fg = plt.figure(i+1)
    fg.set_size_inches(w,h)
    plt.rcParams['font.size'] = 11
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.plot(t,u[:,i],'-',color=clr1,label='Ve(t)')
    plt.plot(t,PAu,'--',color=clr2,label='Vs(t)')
    plt.plot(t,PIDu,':',linewidth=2.5,color=clr3,label='I(t)')
    plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
    if i == 0 or i == 1 or i == 2:
        plt.ylim(-0.1,1.2); plt.yticks(np.arange(-0.1,1.3,0.1))
    elif i == 3:
        plt.ylim(-1.2,1.2); plt.yticks(np.arange(-1.2,1.4,0.2))
    plt.xlabel('t [s]')
    plt.ylabel('Vi(t) [V]')
    plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=3,frameon=False)
    plt.show()
    fg.savefig(signals[i]+'_python.pdf',bbox_inches='tight')
