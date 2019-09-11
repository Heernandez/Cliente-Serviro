import zmq
import random
import json

CLIENT_PORT = "6000"

PUERTOS_SERVIDOR_LIBRE = [ i for i in range(5000,5003)]
PUERTOS_SERVIDOR_ASIGNADO = []
DIC = None

ctx = zmq.Context()

def client_connection():
    #atiende clientes

    sc   = ctx.socket(zmq.REP)
    sc.bind("tcp://*:"+CLIENT_PORT)
    return sc

def server_connection(PORT):
    #se conecta a servidores
    
    ss   = ctx.socket(zmq.REQ)
    ss.connect("tcp://localhost:"+PORT) 

    return ss

def port_asign():
    
    #le  provee a un servidor un puerto por el cual funcionar
    if len(PUERTOS_SERVIDOR_LIBRE) != 0:
        port = random.choice(  PUERTOS_SERVIDOR_LIBRE)
        PUERTOS_SERVIDOR_LIBRE.remove(port)
        PUERTOS_SERVIDOR_ASIGNADO.append(port)
        print("voy a asignar el puerto :",port)
        port = str(port)
        print("Usados :",PUERTOS_SERVIDOR_ASIGNADO)
        return port
    else:
        print("no hay puertosdisponibles para un nuevoservidor")
        return '0'

if __name__ == '__main__':
    print("Proxy Server start at port 6000 ....\nListening .....")
    
    s = client_connection()

    while True:

        m = s.recv_multipart()

        if int(m[0]) == 90:
            
            lis = []
            for i in PUERTOS_SERVIDOR_ASIGNADO:
                lis.append(str(i).encode())
            s.send_multipart(lis)
            
            print("intentando")
            DIC = s.recv_json()
            print(" El diccionario es ",DIC)
            s.send_multipart([b'si me llego '])

        elif int(m[0]) == 1:
            print("me solicitan un puerto ...")
            #conexion de servidor solicitando puerto
            port = port_asign()
            if int(port) != 0:
                #asignacion correcta
                s.send_multipart([ port.encode('utf-8') ])
            else:
                #no hay puertos disponibles
                s.send_multipart([ b'0'] )
        
        elif int(m[0]) == 2:
            '''
            cliente solicitando lista de archivos y
            se le envia el resultado de todos los servidores 
            '''
            print("procesando la solicitud del cliente...")
            aux = []
            for key,value in DIC.items():
                aux.append(key.encode())
            s.send_multipart(aux)
            
        elif int(m[0]) == 3:

            '''
            El cliente solicita uno de los
            archivos para reproducirlo
            '''
            print("Buscando Archivos de Musica...")
            lista = DIC[m[1].decode('utf-8')]
            aux = []
            for i in lista:
                aux.append(i.encode())
            s.send_multipart(aux)
            
        else:
            s.send_multipart([b'None'])
            pass