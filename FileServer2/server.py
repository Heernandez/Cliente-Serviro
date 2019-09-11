import zmq 
import json
import os 
import hashlib

cant = 1024*1024*10
diccionario = {}

def crear_carpeta():
    directorio = os.getcwd()
    carpeta = "/archivos"
    ruta = directorio+carpeta
    try:
        os.stat(ruta)
    except:
        os.mkdir(ruta)
    
    return ruta

ruta = crear_carpeta()

def check_arrival(ArchivoNuevo):
    #comprobar si ya existe un archivo con el mismo nombre
    list = os.listdir(ruta)
    if ArchivoNuevo in list:
        print("el archivo ya existe!")
        return False
    else:
        return True

def download():
    pass

def upload(m):
    #with open(ruta+'/'+str(m[2].decode('utf-8')),'ab') as nf:
    with open(ruta+'/'+"temporal",'ab') as nf:    
        nf.write( m[1] )
        s.send_string("listo")
 
def check_save(m):
    with open(ruta+'/'+"temporal" ,'rb') as f:
        sha256 = hashlib.sha256()
        while True:
            file = f.read(cant)
            if not file:
                break
            else:
                sha256.update(file)
    
    HashServer = sha256.hexdigest()
    if HashServer == m[2].decode():
        rutatemporal = ruta+'/'+"temporal"
        rutanuevo = ruta+'/'+HashServer
        os.rename(rutatemporal,rutanuevo)
        diccionario[HashServer] = m[1].decode()
        return True
    else:
        print("El archivo no pudo ser comprobado ...")
        os.remove(ruta+'/'+"temporal")
        return False

if __name__ == '__main__':
    
    ctx = zmq.Context()
    s   = ctx.socket(zmq.REP)
    s.bind("tcp://*:5555")
    
    
    while True:
        
        m = s.recv_multipart()    
        if int(m[0]) == 1:
            resp = check_arrival(str(m[2].decode()))
            if resp == True:
                s.send_string('1')
            else:    
                s.send_string('0') 

        elif int(m[0]) == 2:
            
            upload(m)
            
        elif int(m[0]) == 3: 
            #verificar el sha256
            resp = check_save(m)
            if resp == True:
                s.send_string("guardado")
            else:
                s.send_string("Ocurrio un error durante la transmision")
        
        elif int(m[0]) == 4:
            lista = diccionario.values()
            s.send_multipart(lista)

    print("Esto no deberia aparecer")