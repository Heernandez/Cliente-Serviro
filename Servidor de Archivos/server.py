import zmq
import os

responseList = {
    # upload Replies
    "upload" : [ 
            {"status" : 0,
             "message" : "Guardado exitoso"
             },
            {"status" : 1,
             "message" : "Ya existe un archivo con el nombre"
             }

    ],
    "download" : [ 
            {"status" : 0,
             "message" : "Descargado con éxito"
             },
            {"status" : 1,
             "message" : "No existe un archivo con el nombre solicitado"
             }

    ],
    "delete":[
            
            {"status" : 0,
             "message" : " fue eliminado con éxito"
            },
            {"status" : 1,
             "message" : " no se encuentra o ya ha sido eliminado..."
             }


    ],
    "list" : [
        {
            "status" : 0,
            "message": "OK"
        },
        {
            "status" : 1,
            "message": "El servidor aún no tiene archivos disponibles"
        }
    ]
}

def create_archivesFile():
    directorio = os.getcwd()
    carpeta = "/archivos"
    ruta = directorio+carpeta
    try:
        os.stat(ruta)
    except:
        os.mkdir(ruta)

    return ruta

ruta = create_archivesFile()

def check_file(fileName):
    # if exists a file in server with the received name, return True, else return False
    list = os.listdir(ruta)
    if fileName in list:
        return True
    else:
        return False

def download(request,s):
    exists = check_file(request["fileName"])
    if  exists:
        with open(ruta+'/'+request["fileName"], 'rb') as f:
            content = f.read()
            f.close()
        
        reply = responseList[request["request"]][0]
        reply["data"] = content
        s.send_pyobj(reply)
       
    else:
        reply = responseList[request["request"]][1]
        s.send_pyobj(reply)

def delete(request,s):

    flag = 1
    exists = check_file(request["fileName"])
    if  exists:
        os.remove(ruta+'/'+request["fileName"])
        flag = 0

    else:
        flag = 1

    reply = dict(responseList[request["request"]][flag])
    reply["message"] = "El archivo " + request["fileName"] + " "+ reply["message"]     
    s.send_pyobj(reply)
       
def upload(request,s):
    
    exists = check_file(request["fileName"])
    flag = 1
    if not exists:
        with open(ruta+'/'+request["fileName"], 'wb') as nf:
            nf.write(request["data"])
            nf.close()
        flag = 0
    else:
        flag = 1
    
    reply = responseList[request["request"]][flag]
    s.send_pyobj(reply)
    
def file_list(request,s):

    fileList = os.listdir(ruta)
    if len(fileList) == 0:
        s.send_pyobj(responseList[request["request"]][1])
    else:
        response = responseList[request["request"]][0]
        response["data"] = fileList
        s.send_pyobj(response)


if __name__ == '__main__':

    ctx = zmq.Context()
    s = ctx.socket(zmq.REP)
    s.bind("tcp://*:5555")

    while True:
        print("El servidor está activo en el puerto 5555...")
        request = s.recv_pyobj() # receive a request
        if request["request"] == "upload":
            # code that receive a file and save on server
            upload(request,s)   
            
        elif request["request"] == "download":
            # code that send a file to a client
            download(request,s)
            
        elif request["request"] == "list":
            # code that send filelist on server
            file_list(request,s)
        
        elif request["request"] == "delete":
            # code that receive a file to delete on server
            delete(request,s)

        else:
            print("The request {} isnot a valid request for this server...").format(request["request"])
            pass
            # its a invalid request
        os.system("cls..") # On Windows O.S
        #os.system("clear") #On Linux O.S

    print("Esto no deberia aparecer")