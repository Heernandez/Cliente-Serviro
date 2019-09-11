

'''
problema P
tiempo de resolucion T
T(P) = T(V) + T(S)  +  t*n/w  + 2n*c --< para mensajes en la red


T(V) = tiempo que le toma al Ventilator descomponer el problema .. t.fijo
T(S) = tiempo que le toma al Sink componer la solucion .. t.fijo

t*T(n)/w

n = numero tareas
t = tiempo de una tarea
w = numero trabajadores

c = tiempo envio mensaje



ventilator : push - pull : worker : push - pull : sink

zguide.zeromq.org/page-all

ver implementacion del work, vent,sink
'''

