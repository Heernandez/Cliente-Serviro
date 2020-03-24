import zmq
import os
from shutil import rmtree

PATH = None
MYLIST = None

ctx = zmq.Context()

def crear_carpeta(PORT):

    global PATH
    directorio = os.getcwd()
    
    carpeta = "/servidor"+PORT
    
    ruta = directorio+carpeta
    try:
        rmtree('servidor'+PORT)
    except:
        print("no borrado")
    
    try:
        
        os.stat(ruta)
    except:
        os.mkdir(ruta)
    PATH = ruta

def update_content():
    
    #cargar lista de archivos disponibles en el servidor en MYLIST
    global MYLIST
    MYLIST = os.listdir(PATH)

def second_connection(PORT):

    PORT = PORT.decode('utf-8')
    print("voy a funcionar en el puerto: ",PORT)    
    
    s = ctx.socket(zmq.REP)
    s.bind("tcp://*:"+PORT)

    crear_carpeta(PORT)

    return s

def first_connection():
    
    s   = ctx.socket(zmq.REQ)
    s.connect("tcp://localhost:6000") #Ip del proxy

    s.send_multipart([b'1'])
    m = s.recv_multipart()
    op = int(m[0].decode('utf-8'))
    if op != 0:
        return second_connection(m[0])
    else:
        print("NO HAY LUGAR PARA UN SERVIDOR MAS")
        return None

def send_list(s):
    '''
    no se va a utilizar ya 
    que la informacion
    no va a pasar por el proxy

    '''
    #envia la lista de canciones
    global MYLIST
    update_content()
    print("preparando para enviar")
    aux = []
    for i in MYLIST:
        aux.append(i.encode())
    
    s.send_multipart(aux)


    pass

def send_file(s,m):
    '''
    envia el archivo que es solicitado
    El nombre del archivo llega en la posicion 1
    '''
    global MYLIST
    if len(MYLIST) == 0:
        update_content()

    aux = m[1].decode('utf-8')
   

    if aux in MYLIST:
        print("enviando :",aux)
        with open(PATH+'/'+aux,'rb') as f:
            file = f.read()
            s.send_multipart([file])
            f.close()
    else:
        #no tiene la cancion el servidor
        s.send_multipart([b'0'])
   
def save_song(s,m):
    
    name = m[1].decode('utf-8')
    file = m[2]

    with open(PATH+'/'+name, 'wb') as f:
        f.write(file)
        f.close()

    s.send_multipart([b'recibido'])
    
def request(s,m):
    
    peticion = m[0].decode('utf-8')

    if peticion == 'solicitud':
        '''
        no se va a utilizar ya 
        que la informacion
        no va a pasar por el proxy

        '''
        send_list(s)
    elif peticion == 'escuchar':
        #envia una parte solicitada
        send_file(s,m)
    elif peticion == 'cancion':
        #recibe partes para guardar
        save_song(s,m)
    else:
        s.send_multipart([b'0'])
  

if __name__ == '__main__':

    s = first_connection()
    if s != None:
        print("Mi Ruta va a ser :",PATH)
        print("soy un servidor")
        print("Actualizando el listado de musica disponible")
        
            
        while True:
            m = s.recv_multipart()
            update_content()
            request(s,m)
            
        print("Esto no deberia aparecer")
    else:
        print("APAGANDO SERVIDOR...")    

    
